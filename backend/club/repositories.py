from .models import Rate, Comment, Product


class RateRepository:

    @staticmethod
    def create_rate(data):
        return Rate.objects.create(**data)
    
    @staticmethod
    def get_rates_of_product(product:Product):
        return Rate.objects.filter(product=product)


class CommentRepository:
    @staticmethod
    def create_comment(data):
        return Comment.objects.create(**data)

    @staticmethod
    def update_comment(comment_id, data):
        comment = CommentRepository.get_comment(comment_id)
        for key, value in data.items():
            setattr(comment, key, value)
        comment.save()
        return comment

    @staticmethod
    def delete_comment(comment_id):
        comment = CommentRepository.get_comment(comment_id)
        comment.delete()

    @staticmethod
    def get_all_comments():
        return Comment.objects.all()
