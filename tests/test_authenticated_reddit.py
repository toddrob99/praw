"""Tests for AuthenticatedReddit class and its mixins."""

from __future__ import print_function, unicode_literals
import warnings
from praw import errors
from .helper import PRAWTest, betamax


class AuthenticatedRedditTest(PRAWTest):
    """Tests authentication from a non-moderator user."""

    def betamax_init(self):
        self.r.login(self.other_non_mod_name, self.other_non_mod_pswd,
                     disable_warning=True)

    @betamax
    def test_create_subreddit(self):
        # Other account is "too new"
        self.r.login(self.un, self.un_pswd, disable_warning=True)
        unique_name = 'PRAW_{0}'.format(self.r.modhash)[:15]
        self.assertRaises(errors.SubredditExists, self.r.create_subreddit,
                          self.sr, 'PRAW test_create_subreddit')
        self.r.create_subreddit(unique_name, 'The %s' % unique_name,
                                'PRAW test_create_subreddit')

    @betamax
    def test_login__deprecation_warning(self):
        with warnings.catch_warnings(record=True) as warning_list:
            self.r.login(self.un, self.un_pswd)
            self.assertEqual(1, len(warning_list))
            self.assertTrue(isinstance(warning_list[0].message,
                                       DeprecationWarning))

    @betamax
    def test_moderator_or_oauth_required__logged_in_from_reddit_obj(self):
        self.assertRaises(errors.ModeratorOrScopeRequired,
                          self.r.get_settings, self.sr)

    @betamax
    def test_moderator_or_oauth_required__logged_in_from_submission_obj(self):
        submission = self.r.get_submission(url=self.comment_url)
        self.assertRaises(errors.ModeratorOrScopeRequired, submission.remove)

    @betamax
    def test_moderator_or_oauth_required__logged_in_from_subreddit_obj(self):
        subreddit = self.r.get_subreddit(self.sr)
        self.assertRaises(errors.ModeratorOrScopeRequired,
                          subreddit.get_settings)

    @betamax
    def test_moderator_required__multi(self):
        sub = self.r.get_subreddit('{0}+{1}'.format(self.sr, 'test'))
        self.assertRaises(errors.ModeratorRequired, sub.get_mod_queue)


class ModFlairMixinTest(PRAWTest):
    def betamax_init(self):
        self.r.login(self.un, self.un_pswd, disable_warning=True)
        self.subreddit = self.r.get_subreddit(self.sr)

    @betamax
    def test_get_flair_list(self):
        self.assertTrue(next(self.subreddit.get_flair_list()))
