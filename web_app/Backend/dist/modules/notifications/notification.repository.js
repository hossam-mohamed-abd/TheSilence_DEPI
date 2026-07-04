"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.NotificationRepository = void 0;
const prisma_1 = __importDefault(require("../../config/prisma"));
class NotificationRepository {
    async getNotifications(userId) {
        return prisma_1.default.notifications.findMany({
            where: {
                user_id: userId,
            },
            orderBy: {
                created_at: "desc",
            },
        });
    }
    async countUnread(userId) {
        return prisma_1.default.notifications.count({
            where: {
                user_id: userId,
                is_read: false,
            },
        });
    }
    async markAsRead(id, userId) {
        return prisma_1.default.notifications.updateMany({
            where: {
                id,
                user_id: userId,
            },
            data: {
                is_read: true,
            },
        });
    }
    async markAllAsRead(userId) {
        return prisma_1.default.notifications.updateMany({
            where: {
                user_id: userId,
                is_read: false,
            },
            data: {
                is_read: true,
            },
        });
    }
    async deleteNotification(id, userId) {
        return prisma_1.default.notifications.deleteMany({
            where: {
                id,
                user_id: userId,
            },
        });
    }
    async deleteAll(userId) {
        return prisma_1.default.notifications.deleteMany({
            where: {
                user_id: userId,
            },
        });
    }
    async create(userId, title, message, type = "system") {
        return prisma_1.default.notifications.create({
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
exports.NotificationRepository = NotificationRepository;
