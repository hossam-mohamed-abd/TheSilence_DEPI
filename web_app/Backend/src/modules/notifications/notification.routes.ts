import { Router } from "express";

import { NotificationController } from "./notification.controller";

import { authMiddleware } from "../../middleware/auth.middleware";

const router = Router();

const controller = new NotificationController();

router.use(authMiddleware);

router.get("/", controller.getNotifications);

router.get("/unread-count", controller.countUnread);

router.patch("/read-all", controller.markAllAsRead);

router.patch("/:id/read", controller.markAsRead);

router.delete("/", controller.deleteAll);

router.delete("/:id", controller.deleteNotification);

export default router;
