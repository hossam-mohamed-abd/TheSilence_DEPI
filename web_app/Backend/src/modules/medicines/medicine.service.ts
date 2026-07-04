import { MedicineRepository }
from './medicine.repository';

export class MedicineService {
  private medicineRepository =
    new MedicineRepository();

  async getFeaturedMedicines(
    page: number
  ) {
    return this
      .medicineRepository
      .getFeaturedMedicines(page);
  }
}