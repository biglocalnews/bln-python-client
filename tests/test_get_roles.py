from bln.client import Client


def test_get_roles():
    """Test methods that get user roles."""
    c = Client(tier="dev")
    c.groupRoles()
    c.projectRoles()
    c.effectiveProjectRoles()
