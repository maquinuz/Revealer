from flask import render_template, redirect, url_for, flash, abort, request,\
    make_response
from flask.ext.login import current_user, login_required
from werkzeug.security import gen_salt
from . import slides
from .forms import SlideshowForm
from .. import slideshows, db
from ..models import Slideshow, Presentation


@slides.route('/slideshows', defaults={'expand': 0})
@slides.route('/slideshows/<int:expand>')
def index(expand):
    return render_template('slides/index.html', expand=expand,
                           slideshows=Slideshow.query.all())


@slides.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload():
    form = SlideshowForm()
    if form.validate_on_submit():
        record = Slideshow(title=form.title.data, user=current_user,
                           description=form.description.data)
        db.session.add(record)
        db.session.commit()

        slideshows.save(form.slides.data, name=str(record.id))

        flash("Slideshow saved.", category='success')
        return redirect(url_for('slides.view', id=record.id))
    return render_template('slides/upload.html', form=form)


@slides.route('/slide/<int:id>/master/')
@login_required
def present(id):
    record = Slideshow.query.filter_by(user=current_user).first()
    if record is not None:
        record.present()  # update last_presented value

        # create the presentation instance and the corresponding key
        pres = Presentation(slideshow_hash=gen_salt(12), slideshow=record)
        db.session.add(pres)
        db.session.commit()
        return render_template('slideshows/%s' % id, user_type='master',
                               mult_id=pres.slideshow_hash)
    flash("You can't control this slideshow.", category='danger')
    return abort(401)


@slides.route('/presentation/stop', methods=('POST',))
@login_required
def stop():
    id = request.form.get('id', 0, type=int)
    record = Presentation.query.get(id)
    if record is not None and record.slideshow.user == current_user:
        record.delete()
        return make_response('OK', 200)
    return make_response('Unauthorized', 401) if record else\
        make_response('Not Found', 404)


@slides.route('/slide/<string:hash>/client/')
def listen(hash):
    record = Presentation.query.filter_by(slideshow_hash=hash).first()
    if record is not None:
        return render_template('slideshows/%s' % record.slideshow.id,
                               user_type='client',
                               mult_id=record.slideshow_hash)
    flash("Invalid slideshow.", category='danger')
    return abort(404)


@slides.route('/slide/<int:id>/viewer/')
def view(id):
    record = Slideshow.query.get(id)
    if record is not None:
        return render_template('slideshows/%s' % id, user_type='viewer')
    flash("Invalid slideshow.", category='danger')
    return abort(404)


@slides.route('/slide/remove/<int:id>')
@login_required
def remove(id):
    record = Slideshow.query.get(id)
    if record and current_user == record.user:
        record.delete()

        flash("Removed slideshow", category="warning")
        return redirect(url_for('slideshow.index'))
    return abort(404) if not record else abort(401)
