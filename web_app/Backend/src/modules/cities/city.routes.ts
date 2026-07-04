import { Router }
from 'express';

import cityController
from './city.controller';

const router = Router();

router.get(
  '/:governorateId',
  cityController.getByGovernorate
);

router.post(
  '/',
  cityController.create
);

export default router;