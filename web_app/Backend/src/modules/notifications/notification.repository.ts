import prisma from "../../config/prisma";

export class NotificationRepository {
  async getNotifications(userId: bigint) {
    return prisma.notifications.findMany({
      where: {
        user_id: userId,
      },
      orderBy: {
        created_at: "desc",
      },
    });
  }

  async countUnread(userId: bigint) {
    return prisma.notifications.count({
      where: {
        user_id: userId,
        is_read: false,
      },
    });
  }

  async markAsRead(id: bigint, userId: bigint) {
    return prisma.notifications.updateMany({
      where: {
        id,
        user_id: userId,
      },
      data: {
        is_read: true,
      },
    });
  }

  async markAllAsRead(userId: bigint) {
    return prisma.notifications.updateMany({
      where: {
        user_id: userId,
        is_read: false,
      },
      data: {
        is_read: true,
      },
    });
  }

  async deleteNotification(id: bigint, userId: bigint) {
    return prisma.notifications.deleteMany({
      where: {
        id,
        user_id: userId,
      },
    });
  }

  async deleteAll(userId: bigint) {
    return prisma.notifications.deleteMany({
      where: {
        user_id: userId,
      },
    });
  }
  async create(
    userId: bigint,
    title: string,
    message: string,
    type = "system",
  ) {
    return prisma.notifications.create({
      data: {
        user_id: userId,
        title,
        message,
        notification_type: type,
        is_read: false,
      },
    });
  }
}
