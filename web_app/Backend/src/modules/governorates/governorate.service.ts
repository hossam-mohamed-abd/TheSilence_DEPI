import governorateRepository from './governorate.repository';

class GovernorateService {
  async getByCountry(
    countryId: number
  ) {
    return governorateRepository.getByCountry(
      countryId
    );
  }

  async create(
    name: string,
    countryId: number
  ) {
    return governorateRepository.create(
      name,
      countryId
    );
  }
}

export default new GovernorateService();