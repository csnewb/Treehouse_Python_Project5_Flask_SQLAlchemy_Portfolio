from flask import Flask, flash
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, url_for, request, redirect
from datetime import datetime
from start_data import projects

db = SQLAlchemy()
app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    project_date = db.Column(db.Date)
    project_url = db.Column(db.String)
    skills = db.Column(db.String)
    description = db.Column(db.String)


@app.route("/", methods=["GET"])
def index():  # /
    all_projects = Project.query.all()
    return render_template("index.html", all_projects=all_projects)


@app.route("/about", methods=["GET"])
def about():  # /about
    all_projects = Project.query.all()
    return render_template('about.html', all_projects=all_projects)


@app.route("/projects/new", methods=['GET', 'POST'])
def new():  # /project/new
    all_projects = Project.query.all()
    if request.method == "POST":
        print("request method == POST")
        # Get form data
        title = request.form.get('title')
        date = request.form.get('date')
        description = request.form.get('desc')
        skills = request.form.get('skills')
        github = request.form.get('github')

        print(f"title: {title}"
              f"\ndate: {date}"
              f"\ndescription: {description}"
              f"\nskills: {skills}"
              f"\ngithub: {github}")

        # Todo: Need a function to convert the datestring into a date
        date_str = date
        project_date = datetime.strptime(date_str, "%Y-%m").date()

        # Create a new project instance
        project = Project(
            title=title,
            project_date=project_date,
            project_url=github,
            skills=skills,
            description=description)

        # Add the project to the session and commit it to the database
        db.session.add(project)
        db.session.commit()

        # Retrieve the actual project ID from the newly created record
        new_project_id = project.id

        # Redirect to the project_details page with the project ID as a parameter
        return redirect(url_for('details', id=new_project_id, all_projects=all_projects))
    else:
        return render_template('projectform.html', all_projects=all_projects)


@app.route("/project/<int:id>", methods=["GET"])
def details(id):  # /project/<int:id>
    all_projects = Project.query.all()
    project = Project.query.get(id)
    print("object found")
    print(f"title: {project.title}"
          f"\ndate: {project.project_date}"
          f"\ndescription: {project.description}"
          f"\nskills: {project.skills}"
          f"\ngithub: {project.project_url}"
          f"\nid: {project.id}")
    # return f"displaying project details for project_id: {project.id}"
    return render_template('detail.html', project=project, all_projects=all_projects)


@app.route("/project/<int:id>/edit", methods=["GET", "POST"])
def edit_project(id):  # /project/<int:id>/edit
    all_projects = Project.query.all()
    project = Project.query.get(id)
    print("object found")
    print(f"title: {project.title}"
          f"\ndate: {project.project_date}"
          f"\ndescription: {project.description}"
          f"\nskills: {project.skills}"
          f"\ngithub: {project.project_url}"
          f"\nid: {project.id}")

    if request.method == "POST":
        # TODO: edit html to display the date
        print("request method == POST")
        # Get form data
        title = request.form.get('title')
        date = request.form.get('date')
        description = request.form.get('desc')
        skills = request.form.get('skills')
        github = request.form.get('github')

        print(f"title: {title}"
              f"\ndate: {date}"
              f"\ndescription: {description}"
              f"\nskills: {skills}"
              f"\ngithub: {github}")

        # convert the datestring into a date
        date_str = date
        project_date = datetime.strptime(date_str, "%Y-%m").date()


        project.title = title
        project.project_date = project_date
        project.description = description
        project.skills = skills
        project.project_url = github

        db.session.commit()

        # Redirect to the project_details page with the project ID as a parameter
        return redirect(url_for('details', id=project.id))
    else:
        return render_template('edit_projectform.html', project=project, all_projects=all_projects)


@app.route("/project/<int:id>/delete", methods=["GET", "POST"])
def delete_project(id):
    project = Project.query.get(id)

    if project:
        db.session.delete(project)
        db.session.commit()

    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    all_projects = Project.query.all()
    return render_template('oops_404.html', all_projects=all_projects), 404


def db_starting_data(projects):
    added = False
    for project in projects:
        title = project['title']
        date_str = project['project_date']
        project_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        print(f"title: {title}")
        query = Project.query.filter_by(title=title).first()
        if query:
            print(f"Project already in database. skipping")
            continue
        else:
            print(f"project not in database... initializing now - {title}")
            project = Project(
                title=title,
                project_date=project_date,
                project_url=project['project_url'],
                skills=project['skills'],
                description=project['description'])

            # Add the project to the session and commit it to the database
            db.session.add(project)
            added = True
    if added:
        db.session.commit()
    print(f"Database Initialized with all Starting Data")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        db_starting_data(projects)
    app.run(host="127.0.0.1", port=8000, debug=True)


