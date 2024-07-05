
from . import admin, group, private
# Если использовать глобальный лейблер, то все хендлеры будут зарегистрированы в том же порядке, в котором они были импортированы

labelers = [admin.admin_labeler, group.labeler]

__all__ = ["labelers"]