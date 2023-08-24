from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Review
from .serializers import ReviewSerializer
from products.models import Product
from users.permissions import IsAuthenticated, IsBuyer


# 상품 후기 리스트
class ReviewList(APIView):
    def get(self, request):
        product = Product.objects.get(pk=request.data.get('product_id'))
        reviews = Review.objects.filter(product=product)
        serializer = ReviewSerializer(reviews, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

# 상품 후기 작성
class CreateReview(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    def post(self, request):
        product = Product.objects.get(pk=request.data.get('product_id'))
        buyer = request.user.buyer

        if buyer and product:
            request_data = request.data.copy()
            request_data['buyer'] = buyer.pk
            request_data['product'] = product.pk
            serializer = ReviewSerializer(data=request_data)

            if serializer.is_valid():        
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetail(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    #  상품 후기 수정
    def patch(self, request):
        buyer = request.user.buyer

        try:
            review = Review.objects.get(pk=request.data.get('review_id'))
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if buyer.pk != review.buyer_id:
            return Response({'error': '리뷰 수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
        elif buyer.pk == review.buyer_id:
            serializer = ReviewSerializer(review, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_401_UNAUTHORIZED)
        

    #  상품 후기 삭제
    def delete(self, request):
        buyer = request.user.buyer

        try:
            review = Review.objects.get(pk=request.data.get('review_id'))
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if buyer.pk != review.buyer_id:
            return Response({'error': '리뷰 삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        review.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)