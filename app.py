from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps

app = Flask(__name__)
app.secret_key = 'change-me-in-production'  # Use os.environ.get('SECRET_KEY') in prod


# ── Auth decorator ────────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user'):
            flash('Please sign in to continue.', 'info')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    # Redirect logged-in users straight to dashboard
    if session.get('user'):
        return redirect(url_for('dashboard'))
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user'):
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        # TODO: replace with real user lookup + password check
        if email and password == 'password':
            session.permanent = remember
            session['user'] = {'email': email, 'name': email.split('@')[0].title()}
            flash('Welcome back!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been signed out.', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    user = session['user']

    # TODO: replace with real data from your database
    stats = {
        'projects':   7,
        'tasks_done': 42,
        'pending':    3,
        'members':    5,
    }
    activity = [
        {'text': 'Project "Alpha" was updated',      'time': '2 min ago'},
        {'text': 'New member joined the workspace',  'time': '1 hr ago'},
        {'text': 'Task "Write docs" marked done',    'time': '3 hrs ago'},
        {'text': 'You created project "Beta"',       'time': 'Yesterday'},
    ]
    tasks = [
        {'title': 'Review pull request #42', 'priority': 'high',   'done': False},
        {'title': 'Update onboarding flow',  'priority': 'medium', 'done': False},
        {'title': 'Write release notes',     'priority': 'low',    'done': False},
        {'title': 'Fix login redirect bug',  'priority': 'high',   'done': True},
    ]

    return render_template('dashboard.html',
        current_user=type('User', (), user)(),  # simple object from dict
        stats=stats,
        activity=activity,
        tasks=tasks,
    )


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True)