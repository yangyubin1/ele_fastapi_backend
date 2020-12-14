import datetime

from models import Base
from sqlalchemy import Column, VARCHAR, INTEGER, DATETIME, TEXT


class UserInfo(Base):
    """
    管理员表
    """
    __tablename__ = "user_info"
    user_id = Column(VARCHAR(32), unique=True, nullable=False, comment="用户id")
    avatar = Column(VARCHAR(256), comment="用户头像")
    balance = Column(INTEGER, default=0, comment="用户账户余额")
    brand_member_new = Column(INTEGER, default=0, comment="名牌选购次数")
    current_address_id = Column(INTEGER, default=0, comment="当前住址ID")
    current_invoice_id = Column(INTEGER, default=0, comment="当前发票ID")
    delivery_card_expire_days = Column(INTEGER, default=0, comment="寄卡超时日期")
    email = Column(VARCHAR(128), unique=True, nullable=True, comment="邮箱")
    gift_amount = Column(INTEGER, default=3, comment="礼物数量")
    city = Column(VARCHAR(20), comment="城市")
    registe_time = Column(DATETIME, comment="注册时间")
    is_active = Column(INTEGER, default=True, comment="是否激活 0=未激活 1=激活")
    is_email_valid = Column(INTEGER, default=False, comment="邮箱是否激活 0=未激活 1=激活")
    is_mobile_valid = Column(INTEGER, default=True, comment="手机是否激活 0=未激活 1=激活")
    mobile = Column(VARCHAR(16), nullable=True, comment="手机号")
    point = Column(INTEGER, default=0, comment="积分")
    username = Column(VARCHAR(20), comment="用户名")
    column_desc = Column(TEXT, nullable=True, comment='信息描述')
    password = Column(VARCHAR(256), comment="用户密码")
    # nickname = Column(VARCHAR(128), comment="管理员昵称")
    # hashed_password = Column(VARCHAR(128), nullable=False, comment="密码")
    # is_active = Column(INTEGER, default=False, comment="邮箱是否激活 0=未激活 1=激活", server_default="0")
    # role_id = Column(INTEGER, comment="角色表")
    __table_args__ = ({'comment': '用户信息表'})
