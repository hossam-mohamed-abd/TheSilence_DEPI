import { Router } from 'express';

import governorateController
from './governorate.controller';

const router = Router();

router.get(
  '/:countryId',
  governorateController.getByCountry
);

router.post(
  '/',
  governorateController.create
);

export default router;