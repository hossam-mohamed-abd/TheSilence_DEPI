import cityRepository
from './city.repository';

class CityService {

  async getByGovernorate(
    governorateId: number
  ) {
    return cityRepository.getByGovernorate(
      governorateId
    );
  }

  async create(
    name: string,
    governorateId: number
  ) {
    return cityRepository.create(
      name,
      governorateId
    );
  }
}

export default new CityService();