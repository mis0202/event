# Generated by Django 3.2 on 2023-07-17 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_department_dev_type_event_list_info_user_phone_num_info_things_source_user_user_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_list',
            name='things_type2',
            field=models.SmallIntegerField(choices=[(0, '创建虚拟机'), (1, '克隆虚拟机'), (2, '新增设备'), (3, '新增云磁盘'), (4, '磁盘故障'), (5, '系统故障'), (6, '光模块故障'), (7, '异常重启'), (8, '设备宕机'), (9, '电源故障'), (10, '链路故障'), (11, '风扇故障'), (12, '内存故障'), (13, 'CPU故障'), (14, '网络故障'), (15, '中间件故障'), (16, '平台故障'), (17, 'VMware生产环境'), (18, 'PaaS平台'), (19, '云桌面'), (20, '云管系统'), (21, '华为云环境'), (22, 'VMware集团云环境'), (23, '英方HA'), (24, 'commvault备份'), (25, '大数据平台'), (26, '测试环境'), (27, '光纤交换机'), (28, '存储'), (29, '服务器'), (30, '操作系统'), (31, '应用和中间件'), (32, '删除虚拟机或回收资源'), (33, '虚拟机快照操作'), (34, '虚拟机配置调整'), (35, '虚拟机扩容'), (36, '虚拟机电源操作'), (37, '共享存储操作'), (38, '配置调整'), (39, '协助排查'), (40, 'VMware环境'), (41, 'paas平台'), (42, '云桌面'), (43, '云管系统'), (44, '华为云环境'), (45, '英方HA'), (46, 'commvault备份'), (47, '大数据平台'), (48, '光纤交换机'), (49, '存储'), (50, '服务器'), (51, '操作系统'), (52, '应用和中间件')], verbose_name='事件分类II'),
        ),
    ]
