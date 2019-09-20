from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import PitchForm,CommentForm,UpdateProfile
from ..models import User,Pitch,Comment
from flask_login import login_required,current_user
from .. import db,photos

import markdown2


# Views
@main.route('/', methods = ['GET','POST'])
def index():

    '''
    View root page function that returns the index page and its data
    '''
    pitch = Pitch.query.filter_by().first()
    title = 'Home'
    pickuplines = Pitch.query.filter_by(category="pickuplines")
    interviewpitch = Pitch.query.filter_by(category = "interviewpitch")
    promotionpitch = Pitch.query.filter_by(category = "promotionpitch")
    productpitch = Pitch.query.filter_by(category = "productpitch")

    

    return render_template('index.html', title = title, pitch = pitch, pickuplines=pickuplines, interviewpitch= interviewpitch, promotionpitch = promotionpitch, productpitch = productpitch)
    
@main.route('/pitch/<int:id>')
def pitch(id):

    '''
    View comment page function that returns the comment details page and its data
    '''
    pitch = get_pitch(id)
    title = f'{pitch.title}'
    comments = Comment.get_comments(pitch.id)

    return render_template('comments.html',title = title,pitch = pitch,comments = comments)





@main.route('/comments/<int:id>')
def pitch_comments(id):
    pitch = get_pitch(id)

    comments = Comment.get_comments(id)
    title = f'All comments for {pitch.title}'
    return render_template('pitch_comments.html',title = title,comments=comments)


@main.route('/comment/<int:id>')
def single_comment(id):
    comment=Comment.query.get(id)
    format_comment = markdown2.markdown(comment.pitch_comment,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('review.html',comment = comment,format_comment=format_comment)




@main.route('/pitch/comment/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_comment(id):

    form = CommentForm()

    pitch = get_pitch(id)

    if form.validate_on_submit():
        title = form.title.data
        comment = form.comment.data

        new_comment = comment(pitch_id=pitch.id,pitch_title=title,pitch_comment=comment,user=current_user)

        new_comment.save_comment()

        return redirect(url_for('.pitch',id = pitch.id ))

    title = f'{pitch.title} comment'
    return render_template('new_review.html',title = title, comment_form=form, pitch=pitch)

@main.route('/user/<uname>')

def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():

        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user_photo = PhotoProfile(pic_path = path,user = user)
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))