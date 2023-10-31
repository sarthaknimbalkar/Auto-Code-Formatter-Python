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

                process = subprocess.Popen(["black", file_path], stdout=subprocess.PIPE)
                output, error = process.communicate()

                if error:
                    flash(f"An error occurred during formatting: {error}", category='error')
                else:
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
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"File removed at {file_path}")
                db.session.delete(file)
                db.session.commit()
                flash('File deleted successfully', category='success')
            else:
                print(f"File not found at {file_path}")
                flash('File not found', category='error')

        return redirect(url_for('views.home'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'py', 'txt'}
