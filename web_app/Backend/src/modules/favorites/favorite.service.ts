import { FavoriteRepository }
from './favorite.repository';

export class FavoriteService {

  private favoriteRepository =
    new FavoriteRepository();

  async toggleFavorite(
    userId: bigint,
    drugId: bigint
  ) {

    const favorite =
      await this.favoriteRepository
        .findFavorite(
          userId,
          drugId
        );

    if (favorite) {

      await this.favoriteRepository
        .removeFavorite(
          userId,
          drugId
        );

      return {
        isFavorite: false,
      };
    }

    await this.favoriteRepository
      .addFavorite(
        userId,
        drugId
      );

    return {
      isFavorite: true,
    };
  }

  async getFavorites(
    userId: bigint
  ) {
    return this.favoriteRepository
      .getFavorites(userId);
  }

  async countFavorites(
    userId: bigint
  ) {
    return this.favoriteRepository
      .countFavorites(userId);
  }
}