import { Router }
from 'express';

import {
  StatisticsController
} from './statistics.controller';

const router =
  Router();

const controller =
  new StatisticsController();

router.get(
  '/',
  controller.getStatistics
);

export default router;