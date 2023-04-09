"""django-rules predicates
"""
import rules

@rules.predicate
def is_creator_or_staff(user, instance):
    """Give access if logged in user is creator of instance or a staff member
    """
    return user.is_staff or user == instance.created_by
