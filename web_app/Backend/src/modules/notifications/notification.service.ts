import { NotificationRepository } from "./notification.repository";

export class NotificationService {
  private repository = new NotificationRepository();

  getNotifications(userId: bigint) {
    return this.repository.getNotifications(userId);
  }

  countUnread(userId: bigint) {
    return this.repository.countUnread(userId);
  }

  markAsRead(id: bigint, userId: bigint) {
    return this.repository.markAsRead(id, userId);
  }

  markAllAsRead(userId: bigint) {
    return this.repository.markAllAsRead(userId);
  }

  deleteNotification(id: bigint, userId: bigint) {
    return this.repository.deleteNotification(id, userId);
  }

  deleteAll(userId: bigint) {
    return this.repository.deleteAll(userId);
  }

  async createWelcomeNotification(userId: bigint) {
    return this.repository.create(
      userId,
      "Welcome to MediSearch 🎉",
      "Welcome to MediSearch. Start searching for medicines, compare prices, and save your favorite medicines.",
      "welcome",
    );
  }
}
