"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.NotificationController = void 0;
const notification_service_1 = require("./notification.service");
const service = new notification_service_1.NotificationService();
class NotificationController {
    async getNotifications(req, res) {
        const data = await service.getNotifications(BigInt(req.userId));
        res.json({
            success: true,
            data,
        });
    }
    async countUnread(req, res) {
        const count = await service.countUnread(BigInt(req.userId));
        res.json({
            success: true,
            count,
        });
    }
    async markAsRead(req, res) {
        await service.markAsRead(BigInt(req.params.id), BigInt(req.userId));
        res.json({
            success: true,
        });
    }
    async markAllAsRead(req, res) {
        await service.markAllAsRead(BigInt(req.userId));
        res.json({
            success: true,
        });
    }
    async deleteNotification(req, res) {
        await service.deleteNotification(BigInt(req.params.id), BigInt(req.userId));
        res.json({
            success: true,
        });
    }
    async deleteAll(req, res) {
        await service.deleteAll(BigInt(req.userId));
        res.json({
            success: true,
        });
    }
}
exports.NotificationController = NotificationController;
