import prisma
from '../../config/prisma';

class CountryRepository {

  async getAll() {
    return prisma.countries.findMany({
      orderBy: {
        name: 'asc'
      }
    });
  }
}

export default
new CountryRepository();