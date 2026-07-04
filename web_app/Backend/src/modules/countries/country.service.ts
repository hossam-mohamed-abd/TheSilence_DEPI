import countryRepository
from './country.repository';

class CountryService {

  async getAll() {
    return countryRepository.getAll();
  }
}

export default
new CountryService();

