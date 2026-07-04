import {
  Request,
  Response,
} from 'express';

import { StatisticsService }
from './statistics.service';

const service =
  new StatisticsService();

export class StatisticsController {

  async getStatistics(
    req: Request,
    res: Response
  ) {
    try {

      const data =
        await service.getStatistics();

      res.json({
        success: true,
        data,
      });

    } catch (error: any) {

      res.status(500).json({
        success: false,
        message: error.message,
      });

    }
  }
}