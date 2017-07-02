import sys, os, random, jwt

sys.path.append(os.path.join(os.getcwd(),'..')) # Appending cwd

# SETTING DJANGO ENVIRONMENT #
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE']='tradecore.settings'
application = get_wsgi_application()
# DONE #

from person.models import *

print('''

            Hello there, human.
            I'm Tyler, and I'm here for demonstration purposes.
            
            If You want me to proceed with default variables such as username and password during the users creation process, type 'start'.
            
            However, if You'd like to change the variables, feel free to do so. To list the variables type 'show'. After You are done with changes, type 'start'.
            If you need anything else, type 'help'
            
            ''')

defaults={
    'name': 'Robot',
    'surname': 'Tyler',
    'email': 'robot@tyler.com',
    'username': 'robot',
    'password': 'password',
}

config=open('config', 'r').readlines()
config_defaults=[int(line.split('=')[1][:-1]) for line in config]

# Config order:
#   [0] = number_of_users
#   [1] = max_posts_per_user
#   [2] = max_likes_per_user

def show():
    for item in defaults:
        print('{}: {}'.format(item,defaults[item]))

def start():
    number_of_users=config_defaults[0]
    max_posts_per_user=config_defaults[1]
    max_likes_per_user =config_defaults[2]
    defaults['password'] = jwt.encode({'password': defaults['password']}, 'tradecore', algorithm='HS256')


    for i in range(0,number_of_users):
        defaults['name'][0].upper()
        defaults['surname'][0].upper()
        name=defaults['name']
        surname='{} {}'.format(defaults['surname'], str(i+1))
        email='{}{}@{}.tc'.format(defaults['name'].lower(),str(i+1), defaults['surname'].lower())
        username='{}{}{}'.format(defaults['name'].lower(),defaults['surname'].lower(),str(i+1))
        password=defaults['password']

        new_user=User(name=name, surname=surname,email=email,username=username,password=password)
        new_user.save()

        print('[+] {} {} => CREATED [+]'.format(new_user.name, new_user.surname))

    print('\n[+] Done [+]\n')

    robots_list = [robot for robot in User.objects.all()]
    used_robots=robots_list

    for robot in robots_list:   # Logging each robot
        random_max = random.randrange(1, max_posts_per_user)
        robot.logged_in=True
        robot.save()
        print('[+] Using: {} [+]'.format(robot.username))
        for i in range(random_max): # Generating posts for current robot
            new_post=Post(author=robot, title='Title {}'.format(i+1), content='Some random content associated with this robot\'s post.')
            print('[+] POST: {} CREATED [+]'.format(new_post.title))
            new_post.save()
        print('\n')
        robot.logged_in=False
        robot.save()

    print('\n')

    # Liking process

    done=False
    while 0 in [post.likes for post in Post.objects.all()]:
        new_user=[0, None]
        all_likes = Post.objects.filter(likes=0)
        try:
            print('\n\t[+] NEW PROCESS [+]')
            if not used_robots:
                print('[!] Renwing used_robots list [!]')
                used_robots=[robot for robot in User.objects.all()]
                print('[!] List renwed: {} [!]'.format(used_robots))
            for robot in used_robots:
                posts_list=[post for post in Post.objects.filter(author=robot)]
                num_posts=len(posts_list)
                if new_user[0]<num_posts:
                    new_user[0]=num_posts
                    new_user[1]=robot

            used_robots.remove(new_user[1])
            print('[+] NOT USED ROBOTS: ', end='')
            print(list(used_robots))

            print('[+] Next robot with the most posts => {} [{} POSTS] [+]\n'.format(new_user[1], new_user[0]))
            user=new_user[1]
            user.logged_in=True
            user.save()
            print('[!] Setting  Logged in flag [!]')

            other_users=User.objects.filter(logged_in=False)
            user.logged_in=False
            user.save()
            print('[!] other_users: {}'.format(other_users))
            other_posts = {}
            for user in other_users:
                other_posts[user]=list(Post.objects.filter(author=user))
            print('[!] other_posts: {} [!]'.format(other_posts))
            print('[!] Commencing liking process [!]')
            for like in range(max_likes_per_user):
                rand_post_key=random.choice(list(other_posts.keys()))
                print('[!] rand_post_key: {}'.format(rand_post_key))
                print('[!] other_posts[rand_post_key]: {} [!]'.format(other_posts[rand_post_key]))
                if other_posts[rand_post_key]:
                    rand_post = random.choice(other_posts[rand_post_key])
                    print('[!] rand_post: {}'.format(rand_post))
                    try:
                            print('\n\t\t[+] NEW LIKE [+]')
                            print('[+] Liking {} POST'.format(rand_post))
                            rand_post.likes+=1
                            rand_post.save()
                            other_posts[rand_post_key].remove(rand_post)
                            print('[!] Saving like [!]\n\n')

                    except Exception as e:
                        print(e)
                        print('Exception 1')
                        break

                else:
                    print('[+] Empty List [+]')
                    pass

        except Exception as e:
            print(e)
            print('Exception 2')
            break

    print('[+] Everything is done [+]')
    print('[+] Overall result is as follows: ')
    results=[result for result in Post.objects.all()]
    for result in results:
        print('- {}: {} LIKES'.format(result, result.likes))


def help():
    for cmd in help:
        print(cmd)

def exit():
    print('\n[!] Exiting [!]')
    sys.exit(1)

cmds={
    'show':show,
    'start':start,
    'exit':exit,
    'help':help,
}

help=[
    '\nshow => Shows the current values for the user attributes',
    'start => Starts the whole process of user registration/login, post creation/liking and outputing the results.',
    'set => Sets the value for user attribute (eg. set name Nikola).',
    'exit => Tyler quits.\n',
]

while 1:
    cmd=input('>>> ')
    try:
        cmds[cmd]()

    except KeyError:
            if cmd.startswith('set'):
                cmd_parse=cmd.split(' ')
                if cmd_parse[3:]:
                    cmd_parse[3:].pop()
                defaults[cmd_parse[1]]=cmd_parse[2]

    except KeyboardInterrupt:
        print('Cya later.')
        sys.exit(1)

# TODO:
#   User creation - DONE
#   User creation random amount of posts
#   User likes other posts
