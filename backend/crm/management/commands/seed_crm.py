from datetime import date, timedelta
from django.core.management.base import BaseCommand
from crm.models import Customer, Contact, Deal, Task


class Command(BaseCommand):
    help = 'Seed CRM with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing data...')
        Task.objects.all().delete()
        Deal.objects.all().delete()
        Contact.objects.all().delete()
        Customer.objects.all().delete()

        today = date.today()

        # Customers
        customers_data = [
            {'name': '张伟', 'company': '星辰科技有限公司', 'email': 'zhangwei@xingchen.com', 'phone': '13800001111', 'status': 'active', 'notes': '大客户，年度合同即将续签'},
            {'name': '李娜', 'company': '蓝海数据科技', 'email': 'lina@lanhai.com', 'phone': '13900002222', 'status': 'prospect', 'notes': '通过行业会议认识，对我们的AI方案感兴趣'},
            {'name': '王强', 'company': '鼎新软件集团', 'email': 'wangqiang@dingxin.com', 'phone': '13700003333', 'status': 'active', 'notes': '已合作两年，目前使用基础套餐'},
            {'name': '赵敏', 'company': '云帆电商', 'email': 'zhaomin@yunfan.com', 'phone': '13600004444', 'status': 'prospect', 'notes': '需要CRM集成方案，预算审批中'},
            {'name': '陈刚', 'company': '锐达制造', 'email': 'chengang@ruida.com', 'phone': '13500005555', 'status': 'inactive', 'notes': '去年合同到期未续签，考虑重新激活'},
        ]
        customers = {c['name']: Customer.objects.create(**c) for c in customers_data}

        # Contacts
        contacts_data = [
            {'customer': customers['张伟'], 'name': '张伟', 'role': 'CEO', 'email': 'zhangwei@xingchen.com', 'phone': '13800001111', 'is_primary': True},
            {'customer': customers['张伟'], 'name': '刘洋', 'role': 'CTO', 'email': 'liuyang@xingchen.com', 'phone': '13800001112', 'is_primary': False},
            {'customer': customers['李娜'], 'name': '李娜', 'role': '采购总监', 'email': 'lina@lanhai.com', 'phone': '13900002222', 'is_primary': True},
            {'customer': customers['王强'], 'name': '王强', 'role': '技术负责人', 'email': 'wangqiang@dingxin.com', 'phone': '13700003333', 'is_primary': True},
            {'customer': customers['赵敏'], 'name': '赵敏', 'role': 'VP of Operations', 'email': 'zhaomin@yunfan.com', 'phone': '13600004444', 'is_primary': True},
        ]
        for c in contacts_data:
            Contact.objects.create(**c)

        # Deals
        deals_data = [
            {'customer': customers['张伟'], 'title': '星辰科技年度续签', 'value': 500000, 'stage': 'negotiation', 'expected_close': today + timedelta(days=15)},
            {'customer': customers['李娜'], 'title': '蓝海数据AI方案POC', 'value': 200000, 'stage': 'qualification', 'expected_close': today + timedelta(days=45)},
            {'customer': customers['王强'], 'title': '鼎新软件升级企业版', 'value': 300000, 'stage': 'proposal', 'expected_close': today + timedelta(days=30)},
            {'customer': customers['赵敏'], 'title': '云帆电商CRM集成', 'value': 150000, 'stage': 'qualification', 'expected_close': today + timedelta(days=60)},
            {'customer': customers['张伟'], 'title': '星辰科技数据分析模块', 'value': 120000, 'stage': 'closed_won', 'expected_close': today - timedelta(days=10)},
        ]
        deals = []
        for d in deals_data:
            deals.append(Deal.objects.create(**d))

        # Tasks
        tasks_data = [
            {'customer': customers['张伟'], 'deal': deals[0], 'title': '准备续签合同草案', 'priority': 'high', 'due_date': today + timedelta(days=5)},
            {'customer': customers['李娜'], 'deal': deals[1], 'title': '安排AI方案演示会议', 'priority': 'medium', 'due_date': today + timedelta(days=7)},
            {'customer': customers['王强'], 'deal': deals[2], 'title': '发送企业版报价单', 'priority': 'high', 'due_date': today + timedelta(days=3)},
            {'customer': customers['赵敏'], 'title': '跟进预算审批进度', 'priority': 'medium', 'due_date': today + timedelta(days=10)},
            {'customer': customers['陈刚'], 'title': '联系陈刚了解重新合作意向', 'priority': 'low', 'due_date': today + timedelta(days=14)},
            {'customer': customers['张伟'], 'title': '收集星辰科技使用反馈', 'priority': 'low', 'due_date': today + timedelta(days=20), 'is_completed': True},
        ]
        for t in tasks_data:
            Task.objects.create(**t)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded: {Customer.objects.count()} customers, '
            f'{Contact.objects.count()} contacts, '
            f'{Deal.objects.count()} deals, '
            f'{Task.objects.count()} tasks'
        ))
