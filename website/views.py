import os
import subprocess

from flask import redirect, Blueprint, render_template, request, flash, send_file, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from . import db
from .models import File

views = Blueprint('views', __name__)

UPLOAD_FOLDER = 'uploads'


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    allowed_formats = ', '.join(['.py', '.txt'])  # List of allowed file formats

    if request.method == 'POST':
        file = request.files.get('file')

        if not file:
            flash('No file uploaded', category='error')
        elif allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)

            # Check if the file already exists
            existing_file = File.query.filter_by(name=filename, user_id=current_user.id).first()
            if existing_file:
                flash('File with the same name already exists', category='error')
            else:
                file.save(file_path)
                """formatting_rules(file_path)"""
                process = subprocess.Popen(["autopep8", "--in-place", file_path], stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                _, error = process.communicate()
                process = subprocess.Popen(["black", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                _, error = process.communicate()

                if process.returncode != 0:
                    flash("File upload successful, but formatting failed. Please check your file's syntax.",
                          category='error')
                else:
                    eval_process = subprocess.Popen(["flake8", file_path], stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE)
                    eval_output, _ = eval_process.communicate()

                    log_filename = f"{filename}_log.txt"
                    log_path = os.path.join(UPLOAD_FOLDER, log_filename)
                    with open(log_path, 'w') as log_file:
                        log_file.write(eval_output.decode('utf-8'))

                    flash(f"Analysis completed. Check {log_filename} for details.", category='success')
                    flash('File uploaded and formatted successfully', category='success')
                new_file = File(name=filename, user_id=current_user.id)
                db.session.add(new_file)
                db.session.commit()
        else:
            flash(f'Unsupported file format. Allowed formats are: {allowed_formats}', category='error')

    # Fetch the updated list of files after deletion
    if request.method == 'GET':
        files = File.query.filter_by(user_id=current_user.id).all()
        return render_template("home.html", user=current_user, files=files)

    files = File.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, files=files)


@views.route('/download_log/<int:file_id>', methods=['GET'])
@login_required
def download_log(file_id):
    file = File.query.get(file_id)

    if file and file.user_id == current_user.id:
        try:
            log_filename = f"{file.name}_log.txt"
            log_path = os.path.join(os.getcwd(), UPLOAD_FOLDER, log_filename)

            print(f"Attempting to download log file from path: {log_path}")

            if os.path.exists(log_path):
                with open(log_path, 'r') as log_file:
                    log_content = log_file.read()

                # Split log content into lines
                log_lines = log_content.split('\n')

                # Initialize counters for each error type
                line_too_long_count = 0
                unused_variable_count = 0
                comparison_to_none_count = 0
                comparison_to_true_false_count = 0
                test_for_membership_count = 0
                test_for_object_identity_count = 0
                do_not_compare_types_count = 0
                do_not_assign_lambda_count = 0
                other_error_count = 0

                for line in log_lines:
                    if 'E501' in line:
                        line_too_long_count += 1
                    elif 'F841' in line:
                        unused_variable_count += 1
                    elif 'E701' in line:
                        comparison_to_none_count += 1
                    elif 'E702' in line:
                        comparison_to_true_false_count += 1
                    elif 'E703' in line:
                        test_for_membership_count += 1
                    elif 'E704' in line:
                        test_for_object_identity_count += 1
                    elif 'E711' in line:
                        do_not_compare_types_count += 1
                    elif 'E712' in line:
                        do_not_assign_lambda_count += 1
                    # Add more conditions for other error types as needed
                    else:
                        other_error_count += 1

                # Calculate the total number of lines in the log
                total_lines = len(log_lines)

                # Calculate the percentage for each error type
                percentage_line_too_long = (line_too_long_count / total_lines) * 100
                percentage_unused_variable = (unused_variable_count / total_lines) * 100
                percentage_comparison_to_none = (comparison_to_none_count / total_lines) * 100
                percentage_comparison_to_true_false = (comparison_to_true_false_count / total_lines) * 100
                percentage_test_for_membership = (test_for_membership_count / total_lines) * 100
                percentage_test_for_object_identity = (test_for_object_identity_count / total_lines) * 100
                percentage_do_not_compare_types = (do_not_compare_types_count / total_lines) * 100
                percentage_do_not_assign_lambda = (do_not_assign_lambda_count / total_lines) * 100
                percentage_other_error = (other_error_count / total_lines) * 100

                # Append the error percentages to the log file
                with open(log_path, 'a') as log_file:
                    log_file.write(
                        f"\nAnalysis completed. {percentage_line_too_long:.2f}% lines too long, {percentage_unused_variable:.2f}% unused variables, "
                        f"\n{percentage_comparison_to_none:.2f}% comparison to None, {percentage_comparison_to_true_false:.2f}% comparison to True/False, "
                        f"\n{percentage_test_for_membership:.2f}% test for membership, {percentage_test_for_object_identity:.2f}% test for object identity, "
                        f"\n{percentage_do_not_compare_types:.2f}% do not compare types, {percentage_do_not_assign_lambda:.2f}% do not assign lambda. "
                        f"\n{percentage_other_error:.2f}% other errors. Check the above for details.")

                return send_file(log_path, as_attachment=True)
            else:
                print(f"Log file not found at {log_path}")
                flash('Log not found', category='error')

        except Exception as e:
            print(f'An error occurred while downloading the log: {e}')
            flash(f'An error occurred while downloading the log: {e}', category='error')

    return redirect(url_for('views.home'))


@views.route('/download/<int:file_id>', methods=['GET'])
@login_required
def download_file(file_id):
    file = File.query.get(file_id)

    if file and file.user_id == current_user.id:
        try:
            file_path = os.path.join(os.getcwd(), UPLOAD_FOLDER, file.name)
            print(f"Attempting to download file from path: {file_path}")

            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True)
            else:
                print(f"File not found at {file_path}")
                flash('File not found', category='error')
        except Exception as e:
            print(f'An error occurred while downloading the file: {e}')
            flash(f'An error occurred while downloading the file: {e}', category='error')
    else:
        flash('File not found', category='error')

    return redirect(url_for('views.home'))


@views.route('/delete/<int:file_id>', methods=['GET', 'POST'])
@login_required
def delete_file(file_id):
    if request.method == 'GET':
        # Render the template with the list of files
        files = File.query.filter_by(user_id=current_user.id).all()
        return render_template("home.html", user=current_user, files=files)

    if request.method == 'POST':
        file = File.query.get(file_id)
        if file and file.user_id == current_user.id:
            file_path = os.path.join(UPLOAD_FOLDER, file.name)
            log_filename = f"{file.name}_log.txt"
            log_path = os.path.join(UPLOAD_FOLDER, log_filename)

            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"File removed at {file_path}")

                # Check and delete the associated log file
                if os.path.exists(log_path):
                    os.remove(log_path)
                    print(f"Log file removed at {log_path}")

                db.session.delete(file)
                db.session.commit()
                flash('File and associated log deleted successfully', category='success')
            else:
                print(f"File not found at {file_path}")
                flash('File not found', category='error')

        return redirect(url_for('views.home'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'py', 'txt'}
