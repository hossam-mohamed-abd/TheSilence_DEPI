import { Router }
from 'express';


import countryController
from './country.controller';

const router = Router();

router.get(
  '/',
  countryController.getAll
);

export default router;