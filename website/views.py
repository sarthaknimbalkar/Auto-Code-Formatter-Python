import os

from flask import redirect, Blueprint, render_template, request, flash, send_from_directory, url_for
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

                new_file = File(name=filename, user_id=current_user.id)
                db.session.add(new_file)
                db.session.commit()
                flash('File uploaded successfully', category='success')
        else:
            flash(f'Unsupported file format. Allowed formats are: {allowed_formats}', category='error')

    files = File.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, files=files)


@views.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    file = File.query.get(file_id)
    if file and file.user_id == current_user.id:
        return send_from_directory(UPLOAD_FOLDER, file.name, as_attachment=True)
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
            db.session.delete(file)
            db.session.commit()
            os.remove(os.path.join(UPLOAD_FOLDER, file.name))
            flash('File deleted successfully', category='success')
        else:
            flash('File not found', category='error')

        return redirect(url_for('views.delete_file', file_id=file_id))  # Redirect to the same page after deletion


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'py'}
