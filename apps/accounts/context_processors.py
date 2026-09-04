from apps.organizations.models import Organization, OrgMember
from apps.notifications.models import Notification

def gameforge_context(request):
    if not request.user.is_authenticated:
        return {}
    
    org_memberships = OrgMember.objects.filter(user=request.user).select_related('organization')
    user_orgs = [m.organization for m in org_memberships]
    
    current_org = None
    if 'current_org_id' in request.session:
        current_org = Organization.objects.filter(id=request.session['current_org_id']).first()
    if not current_org and user_orgs:
        current_org = user_orgs[0]
        request.session['current_org_id'] = current_org.id
        
    unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    
    return {
        'current_org': current_org,
        'user_organizations': user_orgs,
        'unread_notifications_count': unread_count,
    }
