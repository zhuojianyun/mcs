from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm,PostForm1,\
    CommentForm,CommentForm1,InsuranceForm1,InsuranceForm
from .. import db
from ..models import Permission, Role, User, Post, Comment,Insurance
from ..decorators import admin_required, permission_required


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post( name = form.name.data, phnumber = form.phnumber.data,\
        jobaddress = form.jobaddress.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,
                           show_followed=show_followed, pagination=pagination)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts,
                           pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(meetway=form.meetway.data,meetcase=form.meetcase.data,\
                          meetdate=form.meetdate.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items

    ### 问题1：怎么让不同的表单在同一个网页中传递给两个视窗函数？

    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


@main.route('/post2/<int:id>', methods=['GET', 'POST'])
def post2(id):
    post = Post.query.get_or_404(id)
    form = CommentForm1()
    if form.validate_on_submit():
        comment = Comment(meetway=form.meetway.data,meetcase=form.meetcase.data,\
                          meetdate=form.meetdate.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('.post2', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items

    ### 问题1：怎么让不同的表单在同一个网页中传递给两个视窗函数？

    return render_template('post2.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)



@main.route('/post1/<int:id>', methods=['GET', 'POST'])
def insurance(id):
    post = Post.query.get_or_404(id)
    #insurance = Insurance.query.get_or_404(id)
    form = InsuranceForm1()
    if form.validate_on_submit():
        insurance = Insurance(insurname=form.insurname.data,toubaoriqi=form.toubaoriqi.data,\
                          baofei=form.baofei.data,baoer=form.baoer.data, \
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(insurance)
        db.session.commit()
        flash('你的保单已经提交！')
        return redirect(url_for('.insurance', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.insurancese.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.insurancese.order_by(Insurance.timestamp.asc()).paginate(page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],error_out=False)
    insurancese = pagination.items
    return render_template('post1.html', posts=[post], form=form,insurancese=insurancese, pagination=pagination)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMIN):
        abort(403)
    form = PostForm1()
    if form.validate_on_submit():
       #post.body = form.body.data
        post.name = form.name.data
        post.phnumber = form.phnumber.data
        post.career = form.career.data
        post.company = form.company.data
        post.jobaddress = form.jobaddress.data
        post.families = form.families.data
        post.connects = form.connects.data
        post.source = form.source.data
        post.homeaddress =form.homeaddress.data
        post.income = form.income.data
        post.insurance = form.insurance.data
        post.bobies = form.bobies.data
        post.liking = form.liking.data
        post.married = form.married.data


        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    #form.body.data = post.body
    form.name.data = post.name
    form.phnumber.data = post.phnumber
    form.career.data = post.career
    form.company.data = post.company
    form.jobaddress.data = post.jobaddress
    form.families.data = post.families
    form.connects.data = post.connects
    form.source.data = post.source
    form.homeaddress.data = post.homeaddress
    form.income.data = post.income
    form.insurance.data = post.insurance
    form.bobies.data = post.bobies
    form.liking.data = post.liking
    form.married.data = post.married
    return render_template('edit_post.html', form=form)


@main.route('/editcc/<int:id>', methods=['GET', 'POST'])
@login_required
def editcc(id):
    comment = Comment.query.get_or_404(id)
    #if current_user != post.author and \
            #not current_user.can(Permission.ADMIN):
        #abort(403)
    #form = PostForm1()
    form = CommentForm()
    if form.validate_on_submit():
        comment.meetway = form.meetway.data
        comment.meetcase = form.meetcase.data
        comment.meetdate = form.meetdate.data
        comment.meetadress = form.meetadress.data
        comment.meettimese = form.meettimese.data
        comment.beetway = form.beetway.data
        comment.newsabout = form.newsabout.data
        comment.thisthink=form.thisthink.data
        comment.fation = form.fation.data
        comment.planbook = form.planbook.data
        comment.badthing = form.badthing.data
        comment.donething = form.donething.data
        comment.nexttime = form.nexttime.data
        comment.todo = form.todo.data

        db.session.add(comment)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.post', id=comment.id))

    form.meetway.data = comment.meetway
    form.meetcase.data = comment.meetcase
    form.meetdate.data = comment.meetdate
    form.meetadress.data = comment.meetadress
    form.meettimese.data = comment.meettimese
    form.beetway.data = comment.beetway
    form.newsabout.data = comment.newsabout
    form.thisthink.data = comment.thisthink
    form.fation.data = comment.fation
    form.planbook.data = comment.planbook
    form.badthing.data = comment.badthing
    form.donething.data = comment.donething
    form.nexttime.data = comment.nexttime
    form.todo.data = comment.todo
    return render_template('edit_cc.html', form=form)



@main.route('/editii/<int:id>', methods=['GET', 'POST'])
@login_required
def editii(id):
    insurance = Insurance.query.get_or_404(id)
    #if current_user != post.author and \
            #not current_user.can(Permission.ADMIN):
        #abort(403)
    #form = PostForm1()
    form = InsuranceForm()
    if form.validate_on_submit():
        insurname = form.insurname.data
        baodanhao = form.baodanhao.data
        toubaoriqi = form.toubaoriqi.data
        shengxiaoriqi = form.shengxiaoriqi.data
        baodanzhuangtai = form.baodanzhuangtai.data
        jiaofeifangshi = form.jiaofeifangshi.data
        jiaofeiqi = form.jiaofeiqi.data
        baoxianqijian = form.baoxianqijian.data
        shixiaoriqi = form.shixiaoriqi.data
        baofei = form.baofei.data
        baoer = form.baoer.data
        banknumber = form.banknumber.data
        bankname = form.bankname.data
        nextgetmoney = form.nextgetmoney.data
        tbname =  form.tbname.data
        bbname =  form.bbname.data
        syname =  form.syname.data
        jjname = form.syname.data

        db.session.add(insurance)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.editii', id=insurance.id))

    form.insurname.data = insurance.insurname
    form.baodanhao.data = insurance.baodanhao
    form.toubaoriqi.data = insurance.toubaoriqi
    form.shengxiaoriqi.data = insurance.shengxiaoriqi
    form.baodanzhuangtai.data = insurance.baodanzhuangtai
    form.jiaofeifangshi.data = insurance.jiaofeifangshi
    form.jiaofeiqi.data = insurance.jiaofeiqi
    form.baoxianqijian.data =insurance.baoxianqijian
    form.shixiaoriqi.data = insurance.shixiaoriqi
    form.baofei.data = insurance.baofei
    form.baoer.data = insurance.baoer
    form.banknumber.data = insurance.banknumber
    form.bankname.data = insurance.bankname
    form.nextgetmoney.data=insurance.nextgetmoney
    form.tbname.data = insurance.tbname
    form.bbname.data = insurance.bbname
    form.syname.data = insurance.syname
    form.syname.data = insurance.jjname

    return render_template('edit_11.html', form=form)

@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))
