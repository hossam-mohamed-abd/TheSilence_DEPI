import {
  Request,
  Response
} from 'express';

import countryService
from './country.service';

import {
  serializeBigInt
} from '../../utils/bigintSerializer';

class CountryController {

  async getAll(
    req: Request,
    res: Response
  ) {
    const countries =
      await countryService.getAll();

    res.json(
      serializeBigInt(
        countries
      )
    );
  }
}

export default
new CountryController();