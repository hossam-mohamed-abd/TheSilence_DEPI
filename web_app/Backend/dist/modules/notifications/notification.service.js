"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.NotificationService = void 0;
const notification_repository_1 = require("./notification.repository");
class NotificationService {
    repository = new notification_repository_1.NotificationRepository();
    getNotifications(userId) {
        return this.repository.getNotifications(userId);
    }
    countUnread(userId) {
        return this.repository.countUnread(userId);
    }
    markAsRead(id, userId) {
        return this.repository.markAsRead(id, userId);
    }
    markAllAsRead(userId) {
        return this.repository.markAllAsRead(userId);
    }
    deleteNotification(id, userId) {
        return this.repository.deleteNotification(id, userId);
    }
    deleteAll(userId) {
        return this.repository.deleteAll(userId);
    }
    async createWelcomeNotification(userId) {
        return this.repository.create(userId, "Welcome to MediSearch 🎉", "Welcome to MediSearch. Start searching for medicines, compare prices, and save your favorite medicines.", "welcome");
    }
}
exports.NotificationService = NotificationService;
