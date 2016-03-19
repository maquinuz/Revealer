from flask import render_template, redirect, url_for, flash, abort
from flask.ext.login import current_user, login_required
from . import slideshow
from .forms import SlideshowForm, EditSlideshowForm
from .. import slideshows, db
from ..models import Slideshow


@slideshow.route('/slideshows')
def index():
    return render_template('slideshow/index.html',
                           slideshows=Slideshow.query.all())


@slideshow.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload():
    form = SlideshowForm()
    if form.validate_on_submit():
        record = Slideshow(title=form.title.data, user=current_user)
        db.session.add(record)
        db.session.commit()

        slideshows.save(form.slides.data, name=str(record.id))

        flash("Slideshow saved.", category='success')
        return redirect(url_for('slideshow.view', id=record.id))
    return render_template('slideshow/upload.html', form=form)


@slideshow.route('/slide/<int:id>/master/')
@login_required
def present(id):
    record = Slideshow.query.filter_by(user=current_user).first()
    if record is not None:
        return render_template('slideshows/%s' % id, user_type='master',
                               mult_id=id)
    flash("You can't control this slideshow.", category='danger')


@slideshow.route('/slide/<int:id>/client/')
def listen(id):
    record = Slideshow.query.get(id)
    if record is not None:
        return render_template('slideshows/%s' % id, user_type='client',
                               mult_id=id)
    flash("Invalid slideshow.", category='danger')


@slideshow.route('/slide/<int:id>/viewer/')
def view(id):
    record = Slideshow.query.get(id)
    if record is not None:
        return render_template('slideshows/%s' % id, user_type='viewer')
    flash("Invalid slideshow.", category='danger')
    return abort(404)


# subscribe populate_form to template
@slideshow.context_processor
def inject_form():
    def populate_form(slideshow):
        form = EditSlideshowForm()
        form.title.data = slideshow.title
        return form
    return dict(populate_form=populate_form)
