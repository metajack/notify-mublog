# notify-mublog

notify-mublog is a [git](http://git.or.cz) post-receive hook script
that posts to a microblogging site like [Identica](http://identi.ca)
or [Twitter](http://twitter.com).

## License

This code is copyright (c) 2008 by Jack Moffitt <jack@metajack.im> and
is available under the [GPLv3](http://www.gnu.org/licenses/gpl.html).
See `LICENSE.txt` for details.

## Usage

To use notify-mublog, just copy `notify-mublog.py` to your
repository's `.git/hooks` dir and call it `post-receive`. Be sure to
set it executable with `chmod 755 post-receive` as well.

You'll need to set some configuration parameters in the Git repo as well:

* hooks.mublogurl - The microblog update API URL.  For Identica, this
  is http://identi.ca/api/statuses/update.json.  It will be very
  similar for other [Laconica](http://laconi.ca) instances.  For
  Twitter, this URL is http://twitter.com/statuses/update.json.
* hooks.mubloguser - The username on the microblog to post as.
* hooks.mublogpass - The password for the microblog user.
* hooks.commiturl - A URL pattern to use for the Web link to the
  commit.  Use %s in place of the commit hash; it will be substituted
  in upon execution.
