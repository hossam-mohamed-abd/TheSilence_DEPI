import { Request, Response } from "express";
import { NotificationService } from "./notification.service";

const service = new NotificationService();

export class NotificationController {
  async getNotifications(
    req: Request,
    res: Response
  ) {
    const data =
      await service.getNotifications(
        BigInt(req.userId!)
      );

    res.json({
      success: true,
      data,
    });
  }

  async countUnread(
    req: Request,
    res: Response
  ) {
    const count =
      await service.countUnread(
        BigInt(req.userId!)
      );

    res.json({
      success: true,
      count,
    });
  }

  async markAsRead(
    req: Request,
    res: Response
  ) {
    await service.markAsRead(
      BigInt(req.params.id as string),
      BigInt(req.userId!)
    );

    res.json({
      success: true,
    });
  }

  async markAllAsRead(
    req: Request,
    res: Response
  ) {
    await service.markAllAsRead(
      BigInt(req.userId!)
    );

    res.json({
      success: true,
    });
  }

  async deleteNotification(
    req: Request,
    res: Response
  ) {
    await service.deleteNotification(
      BigInt(req.params.id as string),
      BigInt(req.userId!)
    );

    res.json({
      success: true,
    });
  }

  async deleteAll(
    req: Request,
    res: Response
  ) {
    await service.deleteAll(
      BigInt(req.userId!)
    );

    res.json({
      success: true,
    });
  }
}