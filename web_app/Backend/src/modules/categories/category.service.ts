import { CategoryRepository } from './category.repository';

export class CategoryService {

  private categoryRepository =
    new CategoryRepository();

async getHomeCategories() {
  return this.categoryRepository
    .findHomeCategories();
}

}