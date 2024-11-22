from .repositories import RateRepository, CommentRepository, Product


class RateService:

    @staticmethod
    def read_all_rate_of_product(product:Product):
        return RateRepository.get_rates_of_product(product)


class CommentService:
    @staticmethod
    def create_comment(data):
        return CommentRepository.create_comment(data)

    @staticmethod
    def update_comment(comment_id, data):
        return CommentRepository.update_comment(comment_id, data)

    @staticmethod
    def delete_comment(comment_id):
        CommentRepository.delete_comment(comment_id)

    @staticmethod
    def get_all_comments():
        return CommentRepository.get_all_comments()
