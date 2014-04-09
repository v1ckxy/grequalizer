from os import stat, chmod
from stat import S_IMODE
from os.path import isdir

from lib.checks import AbstractPerUserCheck
from lib.util import debug

class ChrootPermissionCheck(AbstractPerUserCheck):
    """
    Checks the chroot directories for all users for desired permissions.
    """

    config_section = "chroot_permissions"
    permissions = None

    def post_init(self):
        """
        Stores some options as property for faster access.
        """
        self.permissions = int(self.options.get_str('octal_permissions'), 8)

    def correct(self, user):
        chroot_path = self.get_chroot_for_user(user)
        debug("setting permissions for %s to %o" % (
            chroot_path, self.permissions))
        if not isdir(chroot_path):
            debug("...directory does not exist. Doing nothing.")
            return
        self.execute_safely(chmod, chroot_path, self.permissions)

    def is_correct(self, user):
        debug("checking directory permissions for %s" % user.pw_name)
        chroot_path = self.get_chroot_for_user(user)
        if not isdir(chroot_path):
            debug("...directory does not exist. Ignoring.")
            return True
        return S_IMODE(stat(chroot_path).st_mode) == self.permissions