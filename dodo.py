import os

run_data = [
    ('python', [
        ('rnn.vec', 'default'),
        ('rnn.clib', 'default'),
        ('gcm.vec', 'default'),
        ('gcm.clib', 'default'),
    ]),
    ('julia', [
        ('rnn.loop', 'default'),
        ('rnn.vec', 'default'),
    ]),
]


def task_bench():
    def datapath(*args):
        return os.path.join('data', *args)

    for lang, args_list in run_data:
        for args in args_list:
            target = datapath(lang, *args)
            yield {
                'name': target,
                'actions': [
                    'mkdir -p $(dirname %(targets)s)',
                    lang + '/cli run ' + ' '.join(args) + ' > %(targets)s',
                ],
                'targets': [
                    target,
                ],
            }
