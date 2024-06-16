
from . import admin, group, private
# Если использовать глобальный лейблер, то все хендлеры будут зарегистрированы в том же порядке, в котором они были импортированы

labelers = [group.labeler, private.labeler, admin.admin_labeler]

__all__ = ["labelers"]