from django.db import models

""" 数据库创建操作：
# 需要用数据库工具链接后创建：
# create database event default charset utf8 collate utf8_general_ci; 
# makemigrations   
# migrate --fake
# 删库重建后需要加 --fake 参数

"""


# 案例：用户管理
class info_user(models.Model):
    """ 用户管理案例表 """
    name = models.CharField(verbose_name="姓名", max_length=16)
    passwd = models.CharField(verbose_name="密码", max_length=16)
    age = models.IntegerField(verbose_name="年龄")
    mail = models.CharField(verbose_name="邮箱", max_length=64)


class department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name="部门名", max_length=32)

    def __str__(self):
        return self.title


class user_info(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=16)
    # mail = models.CharField(verbose_name="邮箱", max_length=16)
    passwd = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name="入职时间", )

    # 数据库做的操作
    # 无约束
    # depart = models.BigIntegerField(verbose_name="部门ID")
    # 1、有约束
    # - to 关联表
    # - to_field 关联表中的那一列
    # 2、django自动
    # - 写的是depart
    # - 生成的时候自动改成depart_id
    # 3、部门表被删除后
    # - 置空（前提是该列允许为空）
    #   depart = models.ForeignKey(verbose_name="部门ID",to="department", null= True, blank=True,to_field="id",on_delete=models.SET_NULL)
    # - 级联删除
    #   depart = models.ForeignKey(verbose_name="部门ID",to="department",to_field="id",on_delete=models.CASCADE)

    depart = models.ForeignKey(verbose_name="部门", to="department", to_field="id", on_delete=models.CASCADE)

    # 在django中做的约束
    gender_choise = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choise)


class user(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=16)
    passwd = models.IntegerField(verbose_name="密码")
    age = models.IntegerField(verbose_name="年龄")
    depart = models.ForeignKey(verbose_name="部门ID", to="department", to_field="id", on_delete=models.CASCADE)
    phone_num = models.IntegerField(verbose_name="手机号")
    mail = models.CharField(verbose_name="邮箱地址", max_length=132)
    # account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name="入职时间")
    birthday = models.DateTimeField(verbose_name="生日")
    # 数据库做的操作
    # 无约束
    # depart = models.BigIntegerField(verbose_name="部门ID")

    # 1、有约束
    # - to 关联表
    # - to_field 关联表中的那一列
    # 2、django自动
    # - 写的是depart
    # - 生成的时候自动改成depart_id
    # 3、部门表被删除后
    # - 置空（前提是该列允许为空）
    depart = models.ForeignKey(verbose_name="部门ID", to="department", null=True, blank=True, to_field="id",
                               on_delete=models.SET_NULL)
    # - 级联删除
    # depart = models.ForeignKey(verbose_name="部门ID", to="department", to_field="id", on_delete=models.CASCADE)

    # 在django中做的约束
    gender_choise = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choise)


class phone_num_info(models.Model):
    """靓号表"""
    phone = models.CharField(verbose_name="手机号", max_length=11)
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2, default=99.00)
    status_choise = (
        (0, "闲置"),
        (1, "占用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choise)

    level_choise = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choise)


# Create your models here.、


""" 云平台工单 """


class things_source(models.Model):
    """ 请求来源表 """
    things_source = models.CharField(verbose_name='请求来源', unique=True, max_length=32)

    def __str__(self):
        return self.things_source


class dev_type(models.Model):
    dev_type = models.CharField(verbose_name='事件分类', unique=True, max_length=32)

    def __str__(self):
        return self.dev_type


# class things_type(models.Model):
#     things_type1_choise = (
#         (0, "新增需求"),
#         (1, "服务请求"),
#         (2, "故障处理"),
#         (3, "技术支持"),
#         (4, "方案变更"),
#     )
#     things_type1 = models.SmallIntegerField(verbose_name='事件分类I', choices=things_type1_choise)
#     things_type2 = models.CharField(verbose_name="事件分类I", max_length=32)


class event_list(models.Model):
    event_number = models.CharField(verbose_name="工单编号", max_length=32)
    get_time = models.DateTimeField(verbose_name="报障日期")
    end_time = models.DateTimeField(verbose_name="完成日期")
    doing_time = models.DurationField(verbose_name="处理时长(分钟数)")

    def save(self, *args, **kwargs):
        self.time_difference = self.end_time - self.get_time
        super().save(*args, **kwargs)

    things_source = models.CharField(verbose_name="请求来源", max_length=64)
    source_user = models.CharField(verbose_name="报障人员", max_length=64)
    dev_type = models.CharField(verbose_name="设备类型", max_length=64)

    things_type1_choise = (
        (0, "新增需求"),
        (1, "服务请求"),
        (2, "故障处理"),
        (3, "技术支持"),
        (4, "方案变更"),
    )
    things_type1 = models.SmallIntegerField(verbose_name="事件分类I", choices=things_type1_choise)

    things_type2_choise = (
        (0, "新增需求2"),
        (1, "服务请求2"),
        (2, "故障处理2"),
        (3, "技术支持2"),
        (4, "方案变更2"),
    )
    things_type2 = models.SmallIntegerField(verbose_name="事件分类II", choices=things_type2_choise)

    level_choise = (
        (0, "不涉及"),
        (1, "一级故障"),
        (2, "二级故障"),
        (3, "三级故障"),
        (4, "四级故障"),
    )
    error_level = models.SmallIntegerField(verbose_name="故障等级", choices=level_choise)
    devs_name = models.TextField(verbose_name="设备名称")
    devs_ip = models.TextField(verbose_name="设备管理IP")
    doing_things = models.TextField(verbose_name="事件处理过程（详细过程）")
    doing_user = models.CharField(verbose_name="处理人", max_length=32)
    destination_user = models.CharField(verbose_name="对接人", max_length=32)
    destination_user_phone = models.CharField(verbose_name="对接人电话", max_length=32)
    location = models.CharField(verbose_name="事件处理地点", max_length=12)
    change_data = models.CharField(verbose_name="是否明确表述及提供必要的变更资料", max_length=64)
    devs_SN = models.CharField(verbose_name="设备SN", max_length=256)
    units_SN = models.CharField(verbose_name="坏件SN", max_length=256)
    new_units_SN = models.CharField(verbose_name="新件SN", max_length=256)
    yes_no_choise = (
        (1, "是"),
        (2, "否"),
    )
    feedback = models.SmallIntegerField(verbose_name="是否已反馈给客户", choices=yes_no_choise)
    leave_over = models.SmallIntegerField(verbose_name="是否需要备注遗留", choices=yes_no_choise)
    note = models.TextField(verbose_name="备注")
    add_work_order_number = models.CharField(verbose_name="新增工单编号和变更单号", max_length=32)
    failure_report = models.SmallIntegerField(verbose_name="是否出具故障报告", choices=yes_no_choise)
