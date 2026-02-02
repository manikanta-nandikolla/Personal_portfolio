from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Q
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Profile, Skill, Project, Experience, 
    Education, Certification, Contact, Testimonial
)

# Register your models here.
admin.site.site_header = "Portfolio Administration"
admin.site.site_title = "Portfolio Admin Portal"
admin.site.index_title = "Welcome to Portfolio Management System"


class BaseModelAdmin(admin.ModelAdmin):
    """Base admin class with common features"""
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }


@admin.register(Profile)
class ProfileAdmin(BaseModelAdmin):
    list_display = ['name', 'title', 'email', 'phone', 'location', 'profile_image_preview']
    list_display_links = ['name']
    search_fields = ['name', 'title', 'email', 'bio']
    readonly_fields = ['profile_image_preview']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'title', 'bio', 'profile_image', 'profile_image_preview')
        }),
        ('Contact Details', {
            'fields': ('email', 'phone', 'location'),
            'classes': ('collapse',)
        }),
        ('Social Media', {
            'fields': ('github', 'linkedin', 'twitter'),
            'classes': ('collapse',)
        }),
        ('Resume', {
            'fields': ('resume',),
            'classes': ('collapse',)
        }),
    )
    
    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" style="border-radius: 50%; width: 100px; height: 100px; object-fit: cover; border: 3px solid #4CAF50;" />',
                obj.profile_image.url
            )
        return "No Image"
    profile_image_preview.short_description = 'Profile Preview'


@admin.register(Skill)
class SkillAdmin(BaseModelAdmin):
    list_display = ['name', 'category', 'proficiency_bar', 'icon_preview']
    list_filter = ['category']
    search_fields = ['name']
    list_editable = ['category']
    ordering = ['-proficiency', 'name']
    
    fieldsets = (
        ('Skill Information', {
            'fields': ('name', 'category', 'proficiency', 'icon')
        }),
    )
    
    def proficiency_bar(self, obj):
        color = '#4CAF50' if obj.proficiency >= 80 else '#FFC107' if obj.proficiency >= 60 else '#F44336'
        return format_html(
            '<div style="width: 200px; background: #e0e0e0; border-radius: 10px; overflow: hidden;">'
            '<div style="width: {}%; background: {}; height: 20px; text-align: center; color: white; font-weight: bold; line-height: 20px;">{}%</div>'
            '</div>',
            obj.proficiency, color, obj.proficiency
        )
    proficiency_bar.short_description = 'Proficiency'
    
    def icon_preview(self, obj):
        return format_html('<i class="{}" style="font-size: 24px; color: #2196F3;"></i>', obj.icon)
    icon_preview.short_description = 'Icon'


@admin.register(Project)
class ProjectAdmin(BaseModelAdmin):
    list_display = ['title', 'thumbnail', 'is_featured_badge', 'tech_stack', 'links', 'created_date', 'is_featured']
    list_filter = ['is_featured', 'created_date']
    search_fields = ['title', 'description', 'technologies']
    list_editable = ['is_featured']
    readonly_fields = ['image_preview', 'created_date']
    date_hierarchy = 'created_date'
    
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'description', 'image', 'image_preview', 'technologies')
        }),
        ('Links & Status', {
            'fields': ('github_link', 'live_link', 'is_featured')
        }),
    )
    
    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.2);" />',
                obj.image.url
            )
        return "No Image"
    thumbnail.short_description = 'Thumbnail'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 500px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = 'Full Preview'
    
    def is_featured_badge(self, obj):
        if obj.is_featured:
            return format_html(
                '<span style="background: #4CAF50; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold;">'
                '<i class="fas fa-star"></i> Featured'
                '</span>'
            )
        return format_html(
            '<span style="background: #9E9E9E; color: white; padding: 5px 15px; border-radius: 20px;">'
            'Regular'
            '</span>'
        )
    is_featured_badge.short_description = 'Status'
    
    def tech_stack(self, obj):
        techs = obj.get_tech_list()[:3]
        badges = ''.join([
            f'<span style="background: #2196F3; color: white; padding: 3px 10px; border-radius: 12px; margin: 2px; display: inline-block; font-size: 11px;">{tech}</span>'
            for tech in techs
        ])
        return format_html(badges)
    tech_stack.short_description = 'Technologies'
    
    def links(self, obj):
        links_html = ''
        if obj.github_link:
            links_html += f'<a href="{obj.github_link}" target="_blank" style="margin-right: 10px;"><i class="fab fa-github" style="font-size: 20px; color: #333;"></i></a>'
        if obj.live_link:
            links_html += f'<a href="{obj.live_link}" target="_blank"><i class="fas fa-external-link-alt" style="font-size: 20px; color: #4CAF50;"></i></a>'
        return format_html(links_html) if links_html else 'No links'
    links.short_description = 'Links'


@admin.register(Experience)
class ExperienceAdmin(BaseModelAdmin):
    list_display = ['position', 'company', 'duration', 'status_badge', 'start_date']
    list_filter = ['is_current', 'start_date']
    search_fields = ['position', 'company', 'description']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Position Details', {
            'fields': ('position', 'company', 'description')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
    )
    
    def duration(self, obj):
        start = obj.start_date.strftime('%b %Y')
        end = 'Present' if obj.is_current else obj.end_date.strftime('%b %Y') if obj.end_date else 'N/A'
        return f"{start} - {end}"
    duration.short_description = 'Duration'
    
    def status_badge(self, obj):
        if obj.is_current:
            return format_html(
                '<span style="background: #4CAF50; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold;">'
                '<i class="fas fa-circle" style="font-size: 8px;"></i> Current'
                '</span>'
            )
        return format_html(
            '<span style="background: #757575; color: white; padding: 5px 15px; border-radius: 20px;">'
            'Past'
            '</span>'
        )
    status_badge.short_description = 'Status'


@admin.register(Education)
class EducationAdmin(BaseModelAdmin):
    list_display = ['degree', 'institution', 'field_of_study', 'grade_badge', 'duration', 'start_date']
    list_filter = ['start_date']
    search_fields = ['degree', 'institution', 'field_of_study']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Education Details', {
            'fields': ('degree', 'institution', 'field_of_study', 'grade')
        }),
        ('Timeline & Description', {
            'fields': ('start_date', 'end_date', 'description')
        }),
    )
    
    def duration(self, obj):
        start = obj.start_date.strftime('%Y')
        end = obj.end_date.strftime('%Y') if obj.end_date else 'Present'
        return f"{start} - {end}"
    duration.short_description = 'Period'
    
    def grade_badge(self, obj):
        if obj.grade:
            return format_html(
                '<span style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold;">'
                '<i class="fas fa-award"></i> {}'
                '</span>',
                obj.grade
            )
        return 'N/A'
    grade_badge.short_description = 'Grade'


@admin.register(Certification)
class CertificationAdmin(BaseModelAdmin):
    list_display = ['name', 'issuing_organization', 'issue_date', 'credential_badge', 'verify_link']
    list_filter = ['issuing_organization', 'issue_date']
    search_fields = ['name', 'issuing_organization', 'credential_id']
    date_hierarchy = 'issue_date'
    
    fieldsets = (
        ('Certification Details', {
            'fields': ('name', 'issuing_organization', 'issue_date')
        }),
        ('Credential Information', {
            'fields': ('credential_id', 'credential_url')
        }),
    )
    
    def credential_badge(self, obj):
        if obj.credential_id:
            return format_html(
                '<code style="background: #f5f5f5; padding: 5px 10px; border-radius: 4px; border: 1px dashed #2196F3;">{}</code>',
                obj.credential_id
            )
        return 'N/A'
    credential_badge.short_description = 'Credential ID'
    
    def verify_link(self, obj):
        if obj.credential_url:
            return format_html(
                '<a href="{}" target="_blank" style="color: #4CAF50; text-decoration: none;">'
                '<i class="fas fa-check-circle"></i> Verify'
                '</a>',
                obj.credential_url
            )
        return 'No URL'
    verify_link.short_description = 'Verification'


@admin.register(Contact)
class ContactAdmin(BaseModelAdmin):
    list_display = ['name', 'email', 'subject', 'status_badge', 'created_at', 'action_buttons']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'subject')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    def status_badge(self, obj):
        if obj.is_read:
            return format_html(
                '<span style="background: #4CAF50; color: white; padding: 5px 15px; border-radius: 20px;">'
                '<i class="fas fa-check-double"></i> Read'
                '</span>'
            )
        return format_html(
            '<span style="background: #FF9800; color: white; padding: 5px 15px; border-radius: 20px; animation: pulse 2s infinite;">'
            '<i class="fas fa-envelope"></i> Unread'
            '</span>'
        )
    status_badge.short_description = 'Status'
    
    def action_buttons(self, obj):
        if not obj.is_read:
            return format_html(
                '<a class="button" href="#" style="background: #2196F3; color: white; padding: 5px 15px; border-radius: 5px; text-decoration: none;">'
                'Mark as Read'
                '</a>'
            )
        return ''
    action_buttons.short_description = 'Actions'
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marked as read.')
    mark_as_read.short_description = "Mark selected as read"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} message(s) marked as unread.')
    mark_as_unread.short_description = "Mark selected as unread"


@admin.register(Testimonial)
class TestimonialAdmin(BaseModelAdmin):
    list_display = ['name', 'position', 'company', 'rating_stars', 'image_thumbnail']
    list_filter = ['rating', 'company']
    search_fields = ['name', 'position', 'company', 'testimonial']
    
    fieldsets = (
        ('Person Information', {
            'fields': ('name', 'position', 'company', 'image')
        }),
        ('Testimonial', {
            'fields': ('testimonial', 'rating')
        }),
    )
    
    def rating_stars(self, obj):
        stars = ''.join(['<i class="fas fa-star" style="color: #FFC107;"></i>' for _ in range(obj.rating)])
        empty_stars = ''.join(['<i class="far fa-star" style="color: #FFC107;"></i>' for _ in range(5 - obj.rating)])
        return format_html(stars + empty_stars)
    rating_stars.short_description = 'Rating'
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover; border: 2px solid #4CAF50;" />',
                obj.image.url
            )
        return format_html(
            '<div style="width: 50px; height: 50px; border-radius: 50%; background: #e0e0e0; display: flex; align-items: center; justify-content: center;">'
            '<i class="fas fa-user" style="color: #999;"></i>'
            '</div>'
        )
    image_thumbnail.short_description = 'Photo'


# Custom Dashboard
class CustomAdminSite(admin.AdminSite):
    site_header = "Portfolio Administration"
    site_title = "Portfolio Admin"
    index_title = "Dashboard"
    
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Get statistics
        extra_context['total_projects'] = Project.objects.count()
        extra_context['featured_projects'] = Project.objects.filter(is_featured=True).count()
        extra_context['total_skills'] = Skill.objects.count()
        extra_context['unread_contacts'] = Contact.objects.filter(is_read=False).count()
        extra_context['total_certifications'] = Certification.objects.count()
        
        return super().index(request, extra_context)