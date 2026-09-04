import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

from apps.accounts.models import User, UserPreference
from apps.organizations.models import Organization, Department, OrgMember
from apps.teams.models import Team, TeamMember
from apps.games.models import Game, GameMilestone
from apps.projects.models import Project, ProjectMember, ProjectRisk
from apps.tasks.models import Task, TaskSprint, TaskComment, TaskTimeLog
from apps.bugs.models import Bug, BugComment
from apps.assets.models import Asset, AssetTag
from apps.versions.models import GameVersion
from apps.builds.models import Build
from apps.releases.models import Release, ReleaseChecklist
from apps.store.models import StoreListing
from apps.players.models import Player
from apps.achievements.models import Achievement, PlayerAchievement
from apps.leaderboards.models import Leaderboard, LeaderboardEntry
from apps.analytics.models import DailyMetric, GameAnalyticsEvent
from apps.monetization.models import InGameItem, Transaction
from apps.notifications.models import Notification
from apps.support.models import SupportTicket, TicketMessage
from apps.reports.models import ReportTemplate
from apps.permissions.models import RolePermission
from apps.audit.models import AuditLog

class Command(BaseCommand):
    help = 'Seeds realistic enterprise demo data into GameForge'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Seeding comprehensive GameForge enterprise demo data..."))

        # 1. Superuser / Admin
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@gameforge.io',
                'first_name': 'Alex',
                'last_name': 'Vance',
                'role': User.Role.SUPER_ADMIN,
                'job_title': 'Chief Technology Officer',
                'department': 'Executive Leadership',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user.set_password('AdminPass123!')
        admin_user.save()
        UserPreference.objects.get_or_create(user=admin_user)

        # 2. Key Staff Members
        staff_data = [
            ('sarah_connor', 'sarah@novaforge.com', 'Sarah', 'Connor', User.Role.ORG_ADMIN, 'Studio Head & GM', 'Executive'),
            ('marcus_fenix', 'marcus@novaforge.com', 'Marcus', 'Fenix', User.Role.PROJECT_MANAGER, 'Lead Technical Producer', 'Production'),
            ('elena_fisher', 'elena@novaforge.com', 'Elena', 'Fisher', User.Role.LEAD_DEVELOPER, 'Principal Graphics Architect', 'Engineering'),
            ('gordon_freeman', 'gordon@novaforge.com', 'Gordon', 'Freeman', User.Role.DEVELOPER, 'Senior Gameplay Engineer', 'Engineering'),
            ('claire_redfield', 'claire@novaforge.com', 'Claire', 'Redfield', User.Role.DESIGNER, 'Lead 3D Environment Artist', 'Art & VFX'),
            ('leon_kennedy', 'leon@novaforge.com', 'Leon', 'Kennedy', User.Role.QA_TESTER, 'QA Strike Lead', 'Quality Assurance'),
            ('sam_porter', 'sam@novaforge.com', 'Sam', 'Porter', User.Role.MARKETING_MANAGER, 'Global Publishing Director', 'Marketing'),
            ('ada_wong', 'ada@novaforge.com', 'Ada', 'Wong', User.Role.SUPPORT_AGENT, 'Senior Player Support Specialist', 'Support'),
        ]

        users = {'admin': admin_user}
        for u, email, fn, ln, role, title, dept in staff_data:
            user_obj, _ = User.objects.get_or_create(
                username=u,
                defaults={
                    'email': email,
                    'first_name': fn,
                    'last_name': ln,
                    'role': role,
                    'job_title': title,
                    'department': dept,
                }
            )
            user_obj.set_password('StudioPass123!')
            user_obj.save()
            UserPreference.objects.get_or_create(user=user_obj)
            users[u] = user_obj

        # 3. Organizations
        org_nova, _ = Organization.objects.get_or_create(
            name='NovaForge Interactive',
            defaults={
                'description': 'Award-winning AAA game development studio specializing in deep cinematic role-playing and tactical action games.',
                'website': 'https://novaforge-games.io',
                'plan_tier': Organization.PlanTier.ENTERPRISE,
                'created_by': users['sarah_connor']
            }
        )
        
        org_mythic, _ = Organization.objects.get_or_create(
            name='Mythic Arc Studios',
            defaults={
                'description': 'Innovative indie & mid-market studio crafting cutting-edge stylized action adventures.',
                'website': 'https://mythicarc.io',
                'plan_tier': Organization.PlanTier.PRO,
                'created_by': users['admin']
            }
        )

        # Assign org memberships
        for user_obj in users.values():
            OrgMember.objects.get_or_create(
                organization=org_nova,
                user=user_obj,
                defaults={'role': OrgMember.Role.ADMIN if user_obj.is_lead_or_higher() else OrgMember.Role.MEMBER}
            )

        # Departments
        depts = ['Core Engineering', 'Technical Art & Shaders', 'Game & Level Design', 'Quality Assurance & Automation', 'LiveOps & Community']
        for d in depts:
            Department.objects.get_or_create(organization=org_nova, name=d, defaults={'lead': users['elena_fisher']})

        # 4. Teams
        team_engine, _ = Team.objects.get_or_create(
            organization=org_nova,
            name='Core Engine & Graphics Squad',
            defaults={'lead': users['elena_fisher'], 'color_code': '#3B82F6', 'description': 'Unreal Engine 5 rendering pipelines, Nanite / Lumen customization, and memory profilers.'}
        )
        team_gameplay, _ = Team.objects.get_or_create(
            organization=org_nova,
            name='Combat & Gameplay Squad',
            defaults={'lead': users['gordon_freeman'], 'color_code': '#10B981', 'description': 'Melee combat physics, animation state machines, AI behavior trees, and player input latency.'}
        )
        team_qa, _ = Team.objects.get_or_create(
            organization=org_nova,
            name='QA & Certification Strike Team',
            defaults={'lead': users['leon_kennedy'], 'color_code': '#EF4444', 'description': 'Smoke testing, performance benchmarking on PS5 / Xbox Series X, crash triage, and TRC compliance.'}
        )

        TeamMember.objects.get_or_create(team=team_engine, user=users['elena_fisher'], defaults={'role_in_team': 'Lead Graphics Architect'})
        TeamMember.objects.get_or_create(team=team_engine, user=users['gordon_freeman'], defaults={'role_in_team': 'Senior Systems Engineer'})
        TeamMember.objects.get_or_create(team=team_gameplay, user=users['gordon_freeman'], defaults={'role_in_team': 'Combat Lead'})
        TeamMember.objects.get_or_create(team=team_gameplay, user=users['claire_redfield'], defaults={'role_in_team': 'Art & Animation Liaison'})
        TeamMember.objects.get_or_create(team=team_qa, user=users['leon_kennedy'], defaults={'role_in_team': 'QA Lead'})

        # 5. Games
        game_aethelgard, _ = Game.objects.get_or_create(
            title='Chronicles of Aethelgard',
            defaults={
                'organization': org_nova,
                'genre': 'Open-World Action RPG',
                'engine': Game.Engine.UNREAL_5,
                'platforms': 'PC (Steam/Epic), PlayStation 5, Xbox Series X/S',
                'status': Game.Status.PRODUCTION,
                'summary': 'Next-gen fantasy open world featuring dynamic seasonal biomes, brutal souls-like swordplay, and deep branch narrative choices.',
                'description': 'Step into the fallen continent of Aethelgard, where ancient deities clash for dominance amidst shattered kingdoms. Built from the ground up in Unreal Engine 5 with full Lumen lighting, Nanite geometry, and spatial audio.',
                'budget': Decimal('4500000.00'),
                'repository_url': 'https://git.internal.novaforge.com/games/aethelgard.git',
                'created_by': users['sarah_connor']
            }
        )

        game_cyberblade, _ = Game.objects.get_or_create(
            title='CyberBlade 2099',
            defaults={
                'organization': org_nova,
                'genre': 'Fast-Paced Cyberpunk Hack-and-Slash',
                'engine': Game.Engine.UNITY_6,
                'platforms': 'PC, PlayStation 5, Nintendo Switch 2',
                'status': Game.Status.BETA,
                'summary': 'High-octane neon slasher with synthwave soundtrack, wall-running mechanics, and fluid katana parry physics.',
                'description': 'A cyberpunk thriller set across dystopian megacity vertical districts. Master high-speed reflex combat, augment your cyberware, and dismantle corrupt mega-corporations.',
                'budget': Decimal('2200000.00'),
                'repository_url': 'https://git.internal.novaforge.com/games/cyberblade.git',
                'created_by': users['marcus_fenix']
            }
        )

        game_starbound, _ = Game.objects.get_or_create(
            title='Starbound Odyssey',
            defaults={
                'organization': org_mythic,
                'genre': 'Procedural Space Exploration Sim',
                'engine': Game.Engine.GODOT_4,
                'platforms': 'PC, macOS, Linux (Steam Deck Verified)',
                'status': Game.Status.TESTING,
                'summary': 'Seamless planetary exploration with real orbital mechanics, ship customization, and planetary trading routes.',
                'budget': Decimal('950000.00'),
                'created_by': users['admin']
            }
        )

        # 6. Projects
        p_combat, _ = Project.objects.get_or_create(
            game=game_aethelgard,
            title='V2 Combat Fluidity & Parry System',
            defaults={
                'organization': org_nova,
                'lead': users['gordon_freeman'],
                'status': Project.Status.IN_PROGRESS,
                'priority': Project.Priority.CRITICAL,
                'progress_percentage': 72,
                'budget': Decimal('350000.00'),
                'description': 'Overhauling hit-stop frame calculation, poise damage gauges, dual-wield animation cancelling, and boss hyper-armor states.'
            }
        )

        p_graphics, _ = Project.objects.get_or_create(
            game=game_aethelgard,
            title='UE5 Lumen GI Optimization for Console',
            defaults={
                'organization': org_nova,
                'lead': users['elena_fisher'],
                'status': Project.Status.IN_PROGRESS,
                'priority': Project.Priority.HIGH,
                'progress_percentage': 60,
                'budget': Decimal('220000.00'),
                'description': 'Targeting 60 FPS Performance Mode on PlayStation 5 and Xbox Series X with dynamic resolution scaling.'
            }
        )

        p_cyber_boss, _ = Project.objects.get_or_create(
            game=game_cyberblade,
            title='Sector 7 Boss Battles & Music Sync',
            defaults={
                'organization': org_nova,
                'lead': users['marcus_fenix'],
                'status': Project.Status.IN_PROGRESS,
                'priority': Project.Priority.HIGH,
                'progress_percentage': 85,
                'budget': Decimal('180000.00'),
                'description': 'Cinematic multi-phase boss encounters with real-time dynamic tempo matching synthwave soundtrack triggers.'
            }
        )

        # 7. Sprints & Tasks
        sprint_12, _ = TaskSprint.objects.get_or_create(
            project=p_combat,
            name='Sprint 12: Weapon Art & Hitbox Tuning',
            defaults={
                'start_date': timezone.now().date(),
                'end_date': timezone.now().date() + timezone.timedelta(days=14),
                'goal': 'Finalize greatsword weight values and perfect parry window timings.'
            }
        )

        task_samples = [
            (p_combat, 'Implement Perfect Parry Slow-Motion Trigger', Task.TaskType.FEATURE, Task.Status.IN_PROGRESS, Task.Priority.CRITICAL, users['gordon_freeman'], 16.0, 10.5),
            (p_combat, 'Add Greatsword Stagger Frames on Heavy Armor', Task.TaskType.FEATURE, Task.Status.TODO, Task.Priority.HIGH, users['gordon_freeman'], 8.0, 0.0),
            (p_combat, 'Audit Boss Deflect Hitboxes on Dragon Tail Sweep', Task.TaskType.BUG_FIX, Task.Status.TESTING, Task.Priority.HIGH, users['leon_kennedy'], 6.0, 5.0),
            (p_combat, '3D Model High-Poly Obsidian Claymore', Task.TaskType.ART, Task.Status.REVIEW, Task.Priority.MEDIUM, users['claire_redfield'], 24.0, 22.0),
            (p_graphics, 'Profile Hardware Ray-Tracing Bounding Box BVH', Task.TaskType.OPTIMIZATION, Task.Status.IN_PROGRESS, Task.Priority.CRITICAL, users['elena_fisher'], 32.0, 26.0),
            (p_graphics, 'Calibrate HDR10 Tone Mapping on OLED Displays', Task.TaskType.FEATURE, Task.Status.COMPLETED, Task.Priority.MEDIUM, users['elena_fisher'], 12.0, 12.0),
            (p_cyber_boss, 'Synchronize Neon Blade Particle Trails with Bass Drops', Task.TaskType.ART, Task.Status.COMPLETED, Task.Priority.HIGH, users['claire_redfield'], 14.0, 14.0),
            (p_cyber_boss, 'Fix Memory Leak During Phase 3 Hologram Clones', Task.TaskType.OPTIMIZATION, Task.Status.TODO, Task.Priority.CRITICAL, users['gordon_freeman'], 18.0, 0.0),
        ]

        for proj, title, ttype, status, priority, assignee, est, act in task_samples:
            t_obj, created = Task.objects.get_or_create(
                project=proj,
                title=title,
                defaults={
                    'task_type': ttype,
                    'status': status,
                    'priority': priority,
                    'assigned_to': assignee,
                    'reporter': users['marcus_fenix'],
                    'estimated_hours': Decimal(str(est)),
                    'actual_hours': Decimal(str(act)),
                    'sprint': sprint_12,
                    'description': f"Technical acceptance criteria for '{title}'. Must pass unit tests and validation checks."
                }
            )
            if created:
                TaskComment.objects.create(
                    task=t_obj,
                    author=assignee or users['admin'],
                    content="Branch created on git. Ready for internal playtesting validation."
                )

        # 8. Bugs
        bug_samples = [
            (game_aethelgard, p_combat, 'GPU Crash (D3D12 Device Removed) on Dragon Breath VFX', Bug.Severity.BLOCKER, Bug.Status.IN_PROGRESS, users['gordon_freeman'], users['leon_kennedy'], 'Cast high-tier dragon flame incantation inside enclosed cavern.'),
            (game_aethelgard, p_combat, 'Player Character Falls Through Floor During Dodge Roll on Wooden Bridges', Bug.Severity.CRITICAL, Bug.Status.CONFIRMED, users['gordon_freeman'], users['leon_kennedy'], 'Perform roll at maximum carry weight over Riverwood Suspension Bridge.'),
            (game_cyberblade, p_cyber_boss, 'Audio Distortion and 100ms Desync on Dolby Atmos Output', Bug.Severity.MAJOR, Bug.Status.OPEN, users['elena_fisher'], users['leon_kennedy'], 'Switch audio device to 7.1 surround sound during intense firefight.'),
            (game_aethelgard, p_graphics, 'Shadow Cascades Flickering on Foliage When Camera Rotates at 120Hz', Bug.Severity.MINOR, Bug.Status.FIXED, users['elena_fisher'], users['leon_kennedy'], 'Enable 120 FPS performance mode in graphics settings.'),
            (game_starbound, None, 'Warp Drive Fuel Count Underflows to Negative 1', Bug.Severity.TRIVIAL, Bug.Status.CLOSED, users['admin'], users['leon_kennedy'], 'Execute warp jump with exactly 0.5 fuel units remaining.'),
        ]

        for g, prj, btitle, sev, bstat, dev, qa, rep in bug_samples:
            b_obj, created = Bug.objects.get_or_create(
                game=g,
                title=btitle,
                defaults={
                    'project': prj,
                    'severity': sev,
                    'status': bstat,
                    'assigned_to': dev,
                    'reporter': qa,
                    'version_found': 'v0.9.4-rc2',
                    'platform': 'PC Windows 11 (DirectX 12)',
                    'steps_to_reproduce': rep,
                    'expected_result': 'Smooth execution without errors or graphical anomalies.',
                    'actual_result': 'Crash to desktop / glitch observed.',
                    'logs_or_stacktrace': '[CrashHandler] Error in D3D12DeviceContext::ExecuteCommandLists -> 0x887A0006 DXGI_ERROR_DEVICE_HUNG'
                }
            )
            if created:
                BugComment.objects.create(
                    bug=b_obj,
                    author=dev or users['admin'],
                    message="Reproduced in debug build. Culprit identified in compute shader memory barrier."
                )

        # 9. Versions & Builds
        ver_10, _ = GameVersion.objects.get_or_create(
            game=game_aethelgard,
            version_number='v1.0.0',
            defaults={
                'release_type': GameVersion.ReleaseType.MAJOR,
                'status': GameVersion.Status.ACTIVE,
                'changelog': '- Initial Worldwide Launch Master\\n- 45 Story Quests & 120 Side Dungeons\\n- Ray Traced Lumen Lighting & Nanite Geometry\\n- 60 FPS Performance Mode on Consoles'
            }
        )

        build_101, _ = Build.objects.get_or_create(
            game=game_aethelgard,
            build_number=101,
            defaults={
                'version': ver_10,
                'platform': Build.Platform.WIN64,
                'status': Build.Status.APPROVED,
                'branch_name': 'release/v1.0.0',
                'git_commit_hash': '7f8b9c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b',
                'file_size_mb': Decimal('68500.00'),
                'developer': users['elena_fisher'],
                'qa_tester': users['leon_kennedy'],
                'qa_notes': 'All 14 smoke test suites passed cleanly. Zero crash rate over 48h soak testing.'
            }
        )

        build_102, _ = Build.objects.get_or_create(
            game=game_aethelgard,
            build_number=102,
            defaults={
                'version': ver_10,
                'platform': Build.Platform.PS5,
                'status': Build.Status.APPROVED,
                'branch_name': 'release/v1.0.0-ps5',
                'git_commit_hash': '4a5b6c7d8e9f0a1b2c3d4e5f6a7b7f8b9c1d2e3f',
                'file_size_mb': Decimal('64200.00'),
                'developer': users['elena_fisher'],
                'qa_tester': users['leon_kennedy'],
                'qa_notes': 'Sony TRC compliance verified. DualSense haptic feedback verified.'
            }
        )

        # 10. Releases
        rel_launch, _ = Release.objects.get_or_create(
            release_code='REL-AETH-001',
            defaults={
                'title': 'Chronicles of Aethelgard Worldwide Launch',
                'game': game_aethelgard,
                'version': ver_10,
                'build': build_101,
                'target_platform': 'Steam, Epic Games, PlayStation 5, Xbox Series X',
                'status': Release.Status.PUBLISHED,
                'scheduled_date': timezone.now(),
                'published_date': timezone.now(),
                'release_notes': 'We are thrilled to present Chronicles of Aethelgard to players worldwide! May your blade strike true in the shattered lands.',
                'approved_by': users['sarah_connor'],
                'created_by': users['marcus_fenix']
            }
        )
        ReleaseChecklist.objects.get_or_create(release=rel_launch, item_text='Platform certification cert pass received (Sony & Microsoft)', defaults={'is_completed': True})
        ReleaseChecklist.objects.get_or_create(release=rel_launch, item_text='Steam store page Day-1 build depot populated', defaults={'is_completed': True})
        ReleaseChecklist.objects.get_or_create(release=rel_launch, item_text='Day-0 anti-cheat and multiplayer backend servers online', defaults={'is_completed': True})

        # 11. Assets
        Asset.objects.get_or_create(
            game=game_aethelgard,
            title='Obsidian Greatsword of the Eclipse',
            defaults={
                'category': Asset.Category.MODEL_3D,
                'format_extension': '.fbx',
                'file_size_mb': Decimal('48.5'),
                'version': 'v2.1',
                'owner': users['claire_redfield'],
                'poly_count': 64000,
                'description': 'Hero prop high-poly weapon mesh with 4K PBR normal and roughness textures.'
            }
        )
        Asset.objects.get_or_create(
            game=game_aethelgard,
            title='Ancient Dragon Roar & Flame SFX Pack',
            defaults={
                'category': Asset.Category.AUDIO,
                'format_extension': '.wav (96kHz / 24-bit)',
                'file_size_mb': Decimal('120.0'),
                'version': 'v1.0',
                'owner': users['claire_redfield'],
                'audio_duration_sec': Decimal('45.5'),
                'description': 'Master spatial audio tracks for boss dragon encounter.'
            }
        )

        # 12. Store Listings
        StoreListing.objects.get_or_create(
            game=game_aethelgard,
            store=StoreListing.PlatformStore.STEAM,
            defaults={
                'headline': 'Enter the shattered realms of Aethelgard in the definitive dark fantasy RPG experience.',
                'short_description': 'Unleash devastating combat combos, master ancient elemental sorcery, and explore breathtaking vistas in a world rendered with Unreal Engine 5.',
                'full_description': 'Aethelgard awaits. Explore dense ancient forests, towering mountain fortresses, and abyssal dungeons in a seamless open world. Customize your warrior with hundreds of weapons and armors.',
                'price': Decimal('59.99'),
                'currency': 'USD',
                'status': StoreListing.Status.PUBLISHED,
                'store_url': 'https://store.steampowered.com/app/gameforge_aethelgard',
                'tags': 'Action RPG, Open World, Souls-like, Dark Fantasy, Story Rich, Masterpiece'
            }
        )

        # 13. Players & Community
        players_data = [
            ('ValkyriePrime', 'valk@games.net', 64, 480.5, Decimal('140.00'), 'US'),
            ('ShadowBlade99', 'shadow@gamers.io', 48, 310.2, Decimal('45.00'), 'DE'),
            ('NordicBeast', 'nordic@gaming.se', 52, 395.0, Decimal('80.00'), 'SE'),
            ('TokyoDrifter', 'tokyo@esports.jp', 70, 620.8, Decimal('210.00'), 'JP'),
            ('CyberGhost', 'ghost@matrix.uk', 35, 180.0, Decimal('15.00'), 'GB'),
            ('GamerX_Pro', 'gamerx@play.com', 82, 890.4, Decimal('350.00'), 'US'),
        ]

        created_players = []
        for uname, em, lvl, ptime, wall, ccode in players_data:
            p_obj, _ = Player.objects.get_or_create(
                username=uname,
                defaults={
                    'email': em,
                    'level': lvl,
                    'total_playtime_hours': Decimal(str(ptime)),
                    'wallet_balance': wall,
                    'country_code': ccode,
                }
            )
            created_players.append(p_obj)

        # 14. Achievements & Leaderboards
        ach_dragon, _ = Achievement.objects.get_or_create(
            game=game_aethelgard,
            code='ACH_SLAY_DRAGON',
            defaults={
                'name': 'Bane of the Wyrmlord',
                'description': 'Defeat Ignis the Eternal Dragon without taking flame damage.',
                'points': 50,
                'tier': Achievement.Tier.GOLD,
                'icon_name': 'trophy-fill'
            }
        )

        ach_parry, _ = Achievement.objects.get_or_create(
            game=game_aethelgard,
            code='ACH_PARRY_MASTER',
            defaults={
                'name': 'Reflexes of Steel',
                'description': 'Execute 100 perfect parries against hostile enemies.',
                'points': 25,
                'tier': Achievement.Tier.SILVER,
                'icon_name': 'shield-shaded'
            }
        )

        for p in created_players[:3]:
            PlayerAchievement.objects.get_or_create(player=p, achievement=ach_dragon)
            PlayerAchievement.objects.get_or_create(player=p, achievement=ach_parry)

        lb_boss, _ = Leaderboard.objects.get_or_create(
            game=game_aethelgard,
            name='Boss Rush Time Trial',
            defaults={
                'metric_type': Leaderboard.MetricType.FASTEST_TIME,
                'sort_order': Leaderboard.SortOrder.ASC,
                'season_name': 'Season 1: Age of Dragons'
            }
        )

        LeaderboardEntry.objects.get_or_create(leaderboard=lb_boss, player=created_players[0], defaults={'score': 245000, 'formatted_score': '04m:05s.00', 'rank': 1})
        LeaderboardEntry.objects.get_or_create(leaderboard=lb_boss, player=created_players[1], defaults={'score': 258000, 'formatted_score': '04m:18s.00', 'rank': 2})
        LeaderboardEntry.objects.get_or_create(leaderboard=lb_boss, player=created_players[2], defaults={'score': 272000, 'formatted_score': '04m:32s.00', 'rank': 3})

        # 15. Monetization & Transactions
        item_bp, _ = InGameItem.objects.get_or_create(
            game=game_aethelgard,
            sku='SKU-AETH-BP-S1',
            defaults={
                'name': 'Season 1 Mythic Battle Pass',
                'item_type': InGameItem.ItemType.BATTLE_PASS,
                'price': Decimal('19.99'),
                'description': 'Unlock 100 tiers of cosmetic armor sets, legendary weapon effects, and currency.'
            }
        )

        item_skin, _ = InGameItem.objects.get_or_create(
            game=game_aethelgard,
            sku='SKU-AETH-SKIN-DRAGON',
            defaults={
                'name': 'Dragonscale Plate Armor Armor Set',
                'item_type': InGameItem.ItemType.SKIN,
                'price': Decimal('14.99'),
                'description': 'Luminescent forged dragonscale cosmetic skin with glowing embers.'
            }
        )

        for p in created_players:
            Transaction.objects.get_or_create(
                player=p,
                game=game_aethelgard,
                item=item_bp,
                defaults={
                    'amount': Decimal('19.99'),
                    'currency': 'USD',
                    'status': Transaction.Status.COMPLETED,
                    'payment_gateway': Transaction.Gateway.STEAM
                }
            )

        # 16. Support Tickets
        SupportTicket.objects.get_or_create(
            player=created_players[0],
            subject='Battle pass points failed to update after server maintenance',
            defaults={
                'category': SupportTicket.Category.BILLING,
                'priority': SupportTicket.Priority.HIGH,
                'status': SupportTicket.Status.RESOLVED,
                'assigned_agent': users['ada_wong'],
                'description': 'Completed level 42 quest right before the hotfix deployment and did not receive the bonus tokens.'
            }
        )

        # 17. Reports & RBAC Matrix
        ReportTemplate.objects.get_or_create(
            title='Executive Studio Summary & Release Deck',
            defaults={
                'report_type': ReportTemplate.ReportType.STUDIO_EXECUTIVE,
                'description': 'High-level synthesis of total milestones, bug resolution metrics, builds, and store performance.'
            }
        )
        ReportTemplate.objects.get_or_create(
            title='QA Defect Burndown & Stability Report',
            defaults={
                'report_type': ReportTemplate.ReportType.QA_DEFECT_VELOCITY,
                'description': 'Detailed breakdown of blocker, critical, and major bugs across target platforms.'
            }
        )

        # Populate permissions
        modules = ['games', 'projects', 'tasks', 'bugs', 'builds', 'assets', 'versions', 'releases', 'store', 'players', 'achievements', 'monetization', 'support', 'reports', 'audit']
        for r_choice, _ in User.Role.choices:
            for m in modules:
                RolePermission.objects.get_or_create(
                    role=r_choice,
                    module_name=m,
                    defaults={
                        'can_view': True,
                        'can_create': r_choice in [User.Role.SUPER_ADMIN, User.Role.ORG_ADMIN, User.Role.PROJECT_MANAGER, User.Role.LEAD_DEVELOPER],
                        'can_edit': r_choice in [User.Role.SUPER_ADMIN, User.Role.ORG_ADMIN, User.Role.PROJECT_MANAGER, User.Role.LEAD_DEVELOPER],
                        'can_approve_release': r_choice in [User.Role.SUPER_ADMIN, User.Role.ORG_ADMIN, User.Role.PROJECT_MANAGER]
                    }
                )

        # Initial Audit Log
        AuditLog.log_activity(
            user=admin_user,
            action='SEED_SYSTEM',
            module='system',
            description='Populated GameForge enterprise studio database with demo data.'
        )

        self.stdout.write(self.style.SUCCESS("GameForge enterprise demo environment seeded successfully!"))
        self.stdout.write(self.style.SUCCESS("Superuser: admin / AdminPass123!"))
        self.stdout.write(self.style.SUCCESS("Staff Users password: StudioPass123!"))
