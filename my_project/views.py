from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Housekeeper, HireRequest, RecruitmentRequest, TransferRequest,HousekeeperRequestType
from .serializer import HousekeeperSerializer, HireRequestSerializer, RecruitmentRequestSerializer, TransferRequestSerializer
from .serializer import DummyHousekeeperSerializer,HousekeeperIDSerializer,DummyHireHousekeeperSerializer,DummyRecruitmentRequestSerializer,DummyTransferRequestSerializer,DeleteHousekeeper,UpdateHireRequest
from.models import Status
from .filter import HousekeeperFilter
from django.db import transaction
from .filter import StatusFilter
from rest_framework.permissions import IsAuthenticated
from .utils import ActionLoggingMixin,send_message
from uuid import UUID
import uuid
from django.core.exceptions import ValidationError

from temporary_discount.models import CustomPackage

from role.permissions import HasPermission

from django.conf import settings
from django.http import HttpResponse
import os





################################filter for request Status####################################################


class RecruitmentListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = RecruitmentRequest.objects.all()
    serializer_class = HousekeeperSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StatusFilter

class HireRequestListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = HireRequest.objects.all()
    serializer_class = HireRequestSerializer
    # filter_backends = [DjangoFilterBackend]
    filterset_class = StatusFilter

class TransferRequestListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = TransferRequest.objects.all()
    serializer_class = TransferRequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StatusFilter
    
    
    
####################################################new API ##############################################################################
class HousekeeperListView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'request_type',
                openapi.IN_QUERY,
                description="Comma-separated list of request types to filter by",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'employment_type',
                openapi.IN_QUERY,
                description="Employment type to filter by",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'nationality_type',
                openapi.IN_QUERY,
                description="Nationality to filter by",
                type=openapi.TYPE_STRING,
                required=False
            ),
        ],
        responses={
            200: openapi.Response(
                description="List of housekeepers",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'name': openapi.Schema(type=openapi.TYPE_STRING),
                            'age': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'gender': openapi.Schema(type=openapi.TYPE_STRING),
                            'nationality': openapi.Schema(type=openapi.TYPE_STRING),
                            'religion': openapi.Schema(type=openapi.TYPE_STRING),
                            'isactive': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'is_available': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'worked_before': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'salary': openapi.Schema(type=openapi.TYPE_NUMBER),
                            'employment_type': openapi.Schema(type=openapi.TYPE_STRING),
                            'monthly_salary': openapi.Schema(type=openapi.TYPE_NUMBER),
                            'pricePerMonth': openapi.Schema(type=openapi.TYPE_NUMBER),
                        }
                    )
                )
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
        }
    )
    
    def get(self, request):
        request_type_ids = request.query_params.get('request_type')
        employment_type_id = request.query_params.get('employment_type')
        nationality_id = request.query_params.get('nationality_type')
        custom_package_id = request.query_params.get('custom_package')

        housekeepers = Housekeeper.objects.all()

    # Filter by request_type_ids
        if request_type_ids:
            try:
                request_type_ids_list = request_type_ids.split(',')
            # Convert to UUIDs
                request_type_ids_list = [uuid.UUID(id) for id in request_type_ids_list]
                housekeeper_ids = HousekeeperRequestType.objects.filter(
                    request_type__id__in=request_type_ids_list
                ).values_list('housekeeper_id', flat=True).distinct()
            
                housekeepers = housekeepers.filter(id__in=housekeeper_ids)
            except ValueError:
                return Response({"error": "Invalid UUID in request_type parameter"}, status=status.HTTP_400_BAD_REQUEST)

    # Filter by employment_type_id
        if employment_type_id:
            try:
                employment_type_uuid = uuid.UUID(employment_type_id)
                housekeepers = housekeepers.filter(
                employment_type__id=employment_type_uuid
                )
            except ValueError:
                return Response({"error": "Invalid UUID in employment_type parameter"}, status=status.HTTP_400_BAD_REQUEST)
        
    
    # Filter by nationality_id
        if nationality_id:
            try:
                nationality_uuid = uuid.UUID(nationality_id)
                housekeepers = housekeepers.filter(
                nationality__id=nationality_uuid
                )
            except ValueError:
                return Response({"error": "Invalid UUID in nationality_type parameter"}, status=status.HTTP_400_BAD_REQUEST)
            
        if custom_package_id:
            try:
                custom_package = CustomPackage.objects.get(id=uuid.UUID(custom_package_id))
                housekeepers = housekeepers.filter(
                nationality__in=custom_package.nationallities.all(),
                employment_type=custom_package.employment_type,
            )
                housekeeper_ids = HousekeeperRequestType.objects.filter(
                request_type=custom_package.request_type
            ).values_list('housekeeper_id', flat=True).distinct()

                housekeepers = housekeepers.filter(id__in=housekeeper_ids)
            
            except CustomPackage.DoesNotExist:
                return Response({"error": "Invalid Custom Package ID"}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"error": "Invalid UUID in custom_package_id parameter"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = HousekeeperSerializer(housekeepers.distinct(), many=True, context={'custom_package': custom_package},)
        else:
            serializer = HousekeeperSerializer(housekeepers.distinct(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
            

    # # Serialize the queryset and return the response
    #     serializer = HousekeeperSerializer(housekeepers.distinct(), many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
        


###############################################

class HousekeeperFilterView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'religion',
                openapi.IN_QUERY,
                description="Filter housekeepers by religion",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'age',
                openapi.IN_QUERY,
                description="Filter housekeepers by age",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'nationality',
                openapi.IN_QUERY,
                description="Filter housekeepers by nationality",
                type=openapi.TYPE_STRING,
                required=False
            ),
        ],
        responses={
            200: openapi.Response(
                description="List of housekeepers",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'name': openapi.Schema(type=openapi.TYPE_STRING),
                            'age': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'gender': openapi.Schema(type=openapi.TYPE_STRING),
                            'nationality': openapi.Schema(type=openapi.TYPE_STRING),
                            'religion': openapi.Schema(type=openapi.TYPE_STRING),
                            'isactive': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'is_available': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'worked_before': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'employment_type': openapi.Schema(type=openapi.TYPE_STRING),
                            'monthly_salary': openapi.Schema(type=openapi.TYPE_NUMBER),
                            'pricePerMonth': openapi.Schema(type=openapi.TYPE_NUMBER),
                        }
                    )
                )
            ),
            400: openapi.Response(
                description="Invalid request parameters",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
        }
    )
    
    def get(self, request, *args, **kwargs):
        religion_id = request.GET.get('religion')
        age = request.GET.get('age')
        nationality_id = request.GET.get('nationality')
        ids = request.GET.getlist('ids')  # Assuming the ids are passed as a list

    # Start with all available housekeepers
        housekeepers = Housekeeper.objects.filter(is_available=True)

    # Apply filters if provided
        if religion_id:
            try:
                religion_uuid = UUID(religion_id)
                housekeepers = housekeepers.filter(religion_id=religion_uuid)
            except ValueError:
                return Response({"error": "Invalid religion UUID format"}, status=400)
    
        if age:
            try:
                age = int(age)
                housekeepers = housekeepers.filter(Age=age)
            except ValueError:
                return Response({"error": "Invalid age format"}, status=400)
    
        if nationality_id:
            try:
                nationality_uuid = UUID(nationality_id)
                housekeepers = housekeepers.filter(nationality_id=nationality_uuid)
            except ValueError:
                return Response({"error": "Invalid nationality UUID format"}, status=400)
    

        serializer = HousekeeperSerializer(housekeepers, many=True)
        return Response(serializer.data)
    
        
        
        

        
        





###################################filter for nationallity, Age, is_avalibale #############################################################

class AvailableHousekeeper(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Housekeeper.objects.all()
    serializer_class = HousekeeperSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HousekeeperFilter
    
    
class HousekeeperBatchDetailView(ActionLoggingMixin,APIView):
    permission_classes = [AllowAny]
    serializer_class = DummyHousekeeperSerializer
    
     
    @swagger_auto_schema(
         manual_parameters=[
             openapi.Parameter(
                'ids',
                openapi.IN_QUERY,
                description="Comma-separated list of IDs",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        # Extract the 'ids' parameter from the query parameters
        ids = request.query_params.get('ids', '')
        

        # Split the 'ids' parameter by commas and convert to integers
        try:
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
                user=request.user if request.user.is_authenticated else None,
                action_type="Error",
                model_name="Housekeeper",
                description="Invalid ID format in get request"
            )
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Query the Housekeeper objects with the given IDs
        housekeepers = Housekeeper.objects.filter(id__in=uuid_list)

        # Serialize the data
        serializer = HousekeeperSerializer(housekeepers, many=True)
        
        
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'uuid_list',
                openapi.IN_QUERY,
                description="Comma-separated list of IDs to delete",
                type=openapi.TYPE_STRING
            )
        ],
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        # Extract the 'ids' parameter from the query parameters
        ids = request.query_params.get('ids', '')

        # Split the 'ids' parameter by commas and convert to integers
        try:
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
                user=request.user if request.user.is_authenticated else None,
                action_type="Error",
                model_name="Housekeeper",
                description="Invalid ID format in delete request"
            )
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the Housekeeper objects with the given IDs
        count, _ = Housekeeper.objects.filter(id__in=uuid_list).delete()
        self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Deleted",
            model_name="Housekeeper",
            description=f"Successfully deleted {count} Housekeeper for IDs: {uuid_list}"
        )

        # Return the count of deleted objects
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
    


class HousekeeperListCreateView(ActionLoggingMixin,generics.ListCreateAPIView):
    queryset = Housekeeper.objects.all()
    serializer_class = HousekeeperSerializer
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'sort_by',
                openapi.IN_QUERY,
                description="Field to sort the results by",
                type=openapi.TYPE_STRING,
                default='Name',
                required=False
            ),
            openapi.Parameter(
                'nationality',
                openapi.IN_QUERY,
                description="Filter housekeepers by nationality",
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
                required=False
            ),
        ],
        responses={
            200: openapi.Response(
                description="List of housekeepers",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'name': openapi.Schema(type=openapi.TYPE_STRING),
                            'age': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'gender': openapi.Schema(type=openapi.TYPE_STRING),
                            'nationality': openapi.Schema(type=openapi.TYPE_STRING),
                            'religion': openapi.Schema(type=openapi.TYPE_STRING),
                            'isactive': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'is_available': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'worked_before': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'employment_type': openapi.Schema(type=openapi.TYPE_STRING),
                            'monthly_salary': openapi.Schema(type=openapi.TYPE_NUMBER),
                            'pricePerMonth': openapi.Schema(type=openapi.TYPE_NUMBER),
                        }
                    )
                )
            )
        }
    ) 
    
    def get_queryset(self):
        queryset = Housekeeper.objects.all()
        sort_by = self.request.GET.get('sort_by', 'Name')
        nationalities = self.request.GET.getlist('nationality')

        if nationalities:
            queryset = queryset.filter(nationality__Nationality__in=nationalities)
            
        if sort_by:
            queryset = queryset.order_by(sort_by)

        return queryset

    
    
    
    def get(self, request, *args, **kwargs):
        # Log the action  
        user = request.user if request.user.is_authenticated else None
        self.log_action(
            user=user,
            action_type="Listed",
            model_name="Housekeeper"
        )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Log the action
        user = request.user if request.user.is_authenticated else None
        self.log_action(
            user=user,
            action_type="Created",
            model_name="Housekeeper"
        )
        return super().post(request, *args, **kwargs)

class HousekeeperDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Housekeeper.objects.all()
    serializer_class = HousekeeperSerializer
    permission_classes = [AllowAny] 


    
class HousekeeperIDsView(generics.GenericAPIView):
    serializer_class= HousekeeperIDSerializer
    def get(self, request, *args, **kwargs):
        housekeepers = Housekeeper.objects.values_list('id', flat=True)
        return Response(housekeepers, status=status.HTTP_200_OK)
    
    
#########################################################################################################

class HireHousekeeperBatchDetailView(ActionLoggingMixin,APIView):
    permission_classes = [AllowAny]
    serializer_class = DummyHireHousekeeperSerializer
     
    @swagger_auto_schema(
         manual_parameters=[
             openapi.Parameter(
                'ids',
                openapi.IN_QUERY,
                description="Comma-separated list of IDs",
                type=openapi.TYPE_STRING
            )
        ]
    )
    
    def get(self, request, *args, **kwargs):
        # Extract the 'ids' parameter from the query parameters
        ids = request.query_params.get('ids', '')

        # Split the 'ids' parameter by commas and convert to integers
        try:
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="HireReguest",
            description="Invalid ID format in request"
            )
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Query the Housekeeper objects with the given IDs
        housekeepers = HireRequest.objects.filter(id__in=uuid_list)

        # Serialize the data
        serializer = HireRequestSerializer(housekeepers, many=True)
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Retrieved",
        model_name="HireReguest",
        description=f"Successfully retrieved {len(housekeepers)} HireRequests for IDs: {uuid_list}"
    )
        
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'ids',
                openapi.IN_QUERY,
                description="Comma-separated list of IDs",
                type=openapi.TYPE_STRING
            )
        ]
    )
    
    
    def delete(self, request, *args, **kwargs):
        # Extract the 'ids' parameter from the query parameters
        ids = request.query_params.get('ids', '')

        # Split the 'ids' parameter by commas and convert to integers
        try:
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="HireRequest",
            description="Invalid ID format in request"
            )
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the Housekeeper objects with the given IDs
        count, _ = HireRequest.objects.filter(id__in=uuid_list).delete()
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Deleted",
        model_name="HireRequest",
        description=f"Successfully deleted {count} HireRequests for IDs: {uuid_list}"
    )
        
        # Return the count of deleted objects
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
    
class HireRequestListCreateView(ActionLoggingMixin,generics.ListCreateAPIView):
    queryset = HireRequest.objects.all()
    serializer_class = HireRequestSerializer
    permission_classes = [AllowAny] 
    
    def check_template_path(request):
        template_name = 'contract_Recruitment.docx'
        template_path = os.path.join(settings.BASE_DIR, 'templates', template_name)
        print(template_path)
        if os.path.exists(template_path):
            print("hhhhhhhhhhhhhhhhhhhhhhh")
            return HttpResponse(f'Template found at: {template_path}')
        else:
            print("notttttttttttttttttttttttttt")
            return HttpResponse(f'Template not found at: {template_path}')
    
    def get(self, request, *args, **kwargs):
        # Log the action  
        user = request.user if request.user.is_authenticated else None
        self.log_action(
            user=user,
            action_type="Listed",
            model_name="HireRequest"
        )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
    
        # Log the action
        user = request.user if request.user.is_authenticated else None
        self.log_action(
            user=user,
            action_type="Created",
            model_name="Housekeeper"
        )
        
        
        order_id = f"{serializer.instance.id}-{uuid.uuid4().hex[:8]}"
        serializer.instance.order_id = order_id
        serializer.instance.save()
        
        hire_request_serializer = HireRequestSerializer(serializer.instance)
    
    # Retrieve all request details and include order_id
        request_details = hire_request_serializer.data.copy()  # Copy serialized data
        request_details['order_id'] = order_id  # Add the order_id to the details
    
    # Send notification to the requester with request details
        phone_number = serializer.validated_data.get('requester_contact')
        test_mode = request.data.get('test_mode', False)
        success, message = send_message(phone_number, request_details, test_mode=test_mode)
    
        return Response({
        'message': message,
        'request_details': request_details  # Include all request details in the response
        }, status=status.HTTP_201_CREATED if success else status.HTTP_500_INTERNAL_SERVER_ERROR, headers=headers)
        # # Retrieve request details
        # request_details = {
        #     'housekeeper': serializer.validated_data.get('housekeeper'),
        #     'requester_contact': serializer.validated_data.get('requester_contact'),
        #     'request_date': serializer.validated_data.get('request_date'),
        #     'duration': serializer.validated_data.get('duration'),
        #     'total_price': serializer.validated_data.get('total_price'),
        #     'status': serializer.validated_data.get('status'),
        # }
        
        # Send notification to the requester with request details
    #     phone_number = serializer.validated_data.get('requester_contact')
        
    #     success, message = send_message(phone_number, request_details, test_mode=test_mode)
    
    #     return Response({
    #     'message': message,
    #     'request_details': request_details 
        
    # }, status=status.HTTP_201_CREATED if success else status.HTTP_500_INTERNAL_SERVER_ERROR, headers=headers)

     

class HireRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HireRequest.objects.all()
    serializer_class = HireRequestSerializer
    permission_classes = [AllowAny] 
    
    
############## update hire request status ####################################
class HousekeeperBatchStatusUpdateView(ActionLoggingMixin,APIView):
    serializer_class= UpdateHireRequest
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'ids',
                openapi.IN_QUERY,
                description="Comma-separated list of IDs",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="New status value",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    
    
    @transaction.atomic 
    def patch(self, request, *args, **kwargs):
        # Extract the 'ids' and 'status' parameters from the query parameters
        ids = request.query_params.get('ids', '')
        uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        new_status_name = request.query_params.get('status', '')
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Patch Requested",
        model_name="HireRequest",
        description=f"Patch request with IDs: {ids} and new status: {new_status_name}"
    )

        # Split the 'ids' parameter by commas and convert to integers
        try:
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="HireRequest",
            description="Invalid ID format in patch request"
        )
            
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        if not new_status_name:
            return Response({"error": "Status value is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Status object based on the provided status name
        try:
            new_status = Status.objects.get(Status=new_status_name)
        except Status.DoesNotExist:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="HireRequest",
            description=f"Status '{new_status_name}' does not exist."
        )
            return Response({"error": f"Status '{new_status_name}' does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Query the Housekeeper objects with the given IDs
        housekeepers = HireRequest.objects.filter(id__in=uuid_list)
        if not housekeepers.exists():
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="HireRequest",
            description="No Hire Requests found for the provided IDs."
        )
            return Response({"error": "No Hire Requests found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        # Update the status field for the queried Housekeeper objects
        housekeepers.update(status=new_status)
        
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Updated",
        model_name="HireRequest",
        description=f"Successfully updated status for IDs: {ids} to {new_status_name}"
    )
                
        # Update Status and Housekeeper Availability
        for hire_request in housekeepers:
            hire_request.status = new_status
            hire_request.save() # Save to trigger the update
            

            if new_status.Status == "Approved":
                housekeeper = hire_request.housekeeper
                housekeeper.is_available = False
                housekeeper.save()
            else:
                housekeeper = hire_request.housekeeper
                housekeeper.is_available = True
                housekeeper.save()
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Updated",
        model_name="HireRequest",
        description=f"Successfully updated status for IDs: {ids} to {new_status_name}"
    )
                
                   
        return Response({"message": "Status updated successfully."}, status=status.HTTP_200_OK)
     
        
    
    
################################################################################

class RecruitmentRequestBatchDetailView(ActionLoggingMixin,APIView):
    permission_classes = [AllowAny]
    serializer_class = DummyRecruitmentRequestSerializer
     
    @swagger_auto_schema(
         manual_parameters=[
             openapi.Parameter(
                'ids',
                openapi.IN_QUERY,
                description="Comma-separated list of IDs",
                type=openapi.TYPE_STRING
            )
        ]
    )
    
    def get(self, request, *args, **kwargs):
        # Extract the 'ids' parameter from the query parameters
        ids = request.query_params.get('ids', '')

        # Split the 'ids' parameter by commas and convert to integers
        try:
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="RecruitmentRequest",
            description="Invalid ID format in request"
            )
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Query the Housekeeper objects with the given IDs
        housekeepers = RecruitmentRequest.objects.filter(id__in=uuid_list)

        # Serialize the data
        serializer = RecruitmentRequestSerializer(housekeepers, many=True)
        self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Retrieved",
            model_name="RecruitmentRequest",
            description=f"Successfully retrieved {len(housekeepers)} HireRequests for IDs: {ids}"
        )
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'ids',
                openapi.IN_QUERY,
                description="Comma-separated list of IDs",
                type=openapi.TYPE_STRING
            )
        ]
    )
    
    
    def delete(self, request, *args, **kwargs):
        # Extract the 'ids' parameter from the query parameters
        ids = request.query_params.get('ids', '')

        # Split the 'ids' parameter by commas and convert to integers
        try:
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="RecruitmentRequest",
            description="Invalid ID format in request"
            )
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the Housekeeper objects with the given IDs
        count, _ = RecruitmentRequest.objects.filter(id__in=uuid_list).delete()
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Deleted",
        model_name="RecruitmentRequest",
        description=f"Successfully deleted {count} RecruitmentRequest for IDs: {ids}"
    )

        # Return the count of deleted objects
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
    

    

class RecruitmentRequestListCreateView(ActionLoggingMixin,generics.ListCreateAPIView):
    queryset = RecruitmentRequest.objects.all()
    serializer_class = RecruitmentRequestSerializer
    permission_classes = [AllowAny] 
    
    def get(self, request, *args, **kwargs):
        # Log the action  
        user = request.user if request.user.is_authenticated else None
        self.log_action(
            user=user,
            action_type="Listed",
            model_name="RecruitmentRequest",
        )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create the recruitment request instance
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
    
        # Log the action
        user = request.user if request.user.is_authenticated else None
        self.log_action(
            user=user,
            action_type="Created",
            model_name="RecruitmentRequest"
        )
        
        order_id = f"{serializer.instance.id}-{uuid.uuid4().hex[:8]}"
        serializer.instance.order_id = order_id
        serializer.instance.save()
        
        recruitment_request_serializer = RecruitmentRequestSerializer(serializer.instance)
    
    
        request_details = recruitment_request_serializer.data.copy()  
        request_details['order_id'] = order_id 
    
        phone_number = serializer.validated_data.get('requester_contact')
        test_mode = request.data.get('test_mode', False)
        success, message = send_message(phone_number, request_details, test_mode=test_mode)
    
        return Response({
        'message': message,
        'request_details': request_details  # Include all request details in the response
        }, status=status.HTTP_201_CREATED if success else status.HTTP_500_INTERNAL_SERVER_ERROR, headers=headers)
        
    #     test_mode = request.data.get('test_mode', False)
    #     # Retrieve request details
    #     request_details = {
    #         'housekeeper': serializer.validated_data.get('housekeeper'),
    #         'requester':serializer.validated_data.get('requester'),
    #         'requester_contact': serializer.validated_data.get('requester_contact'),
    #         'request_date': serializer.validated_data.get('request_date'),
    #         'visa_status':serializer.validated_data.get('visa_status'),
    #         'status': serializer.validated_data.get('status'),
    #     }
        
    #     # Send notification to the requester with request details
    #     phone_number = serializer.validated_data.get('requester_contact')
    #     send_message(phone_number, request_details,test_mode=test_mode)
    #     print(send_message)
        
    #     success, message = send_message(phone_number, request_details, test_mode=test_mode)
    
    #     return Response({
    #     'message': message
    # }, status=status.HTTP_201_CREATED if success else status.HTTP_500_INTERNAL_SERVER_ERROR, headers=headers)

     


class RecruitmentRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecruitmentRequest.objects.all()
    serializer_class = RecruitmentRequestSerializer
    permission_classes = [AllowAny] 
    
    
    ########## updating ################################
class RecruitmentBatchStatusUpdateView(ActionLoggingMixin,APIView):
    serializer_class= UpdateHireRequest
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'ids',
                openapi.IN_QUERY,
                description="Comma-separated list of IDs",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="New status value",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    
    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        # Extract the 'ids' and 'status' parameters from the query parameters
        ids = request.query_params.get('ids', '')
        new_status_name = request.query_params.get('status', '')
        
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Patch Requested",
        model_name="RecruitmentRequest",
        description=f"Patch request with IDs: {ids} and new status: {new_status_name}"
    )

        # Split the 'ids' parameter by commas and convert to integers
        try:
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="RecruitmentRequest",
            description="Invalid ID format in patch request"
        )
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        if not new_status_name:
            return Response({"error": "Status value is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Status object based on the provided status name
        try:
            new_status = Status.objects.get(Status=new_status_name)
        except Status.DoesNotExist:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="RecruitmentRequest",
            description=f"Status '{new_status_name}' does not exist."
        )
            return Response({"error": f"Status '{new_status_name}' does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Query the Housekeeper objects with the given IDs
        Recruitment = RecruitmentRequest.objects.filter(id__in=uuid_list)

        if not Recruitment.exists():
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="RecruitmentRequest",
            description="No Recruitment Requests found for the provided IDs."
        )
            return Response({"error": "No Recruitment Requests found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        # Update the status field for the queried Housekeeper objects
        Recruitment.update(status=new_status)
        
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Updated",
        model_name="RecruitmentRequest",
        description=f"Successfully updated status for IDs: {ids} to {new_status_name}"
    )
        
        for hire_request in Recruitment:
            hire_request.status = new_status
            hire_request.save()  # Save to trigger the update

            if new_status.Status == "Approved":
                housekeeper = hire_request.housekeeper
                housekeeper.is_available = False
                housekeeper.save()
            else:
                housekeeper = hire_request.housekeeper
                housekeeper.is_available = True
                housekeeper.save()
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Updated",
            model_name="RecruitmentRequest",
            description=f"Successfully updated status for IDs: {ids} to {new_status_name}"
    )
                
        
                   
        return Response({"message": "Status updated successfully."}, status=status.HTTP_200_OK)
        
    
    
    
    
########################################################################################################


class TransferRequestBatchDetailView(ActionLoggingMixin,APIView):
    permission_classes = [AllowAny]
    serializer_class = DummyTransferRequestSerializer
     
    @swagger_auto_schema(
         manual_parameters=[
             openapi.Parameter(
                'ids',
                openapi.IN_QUERY,
                description="Comma-separated list of IDs",
                type=openapi.TYPE_STRING
            )
        ]
    )
    
    def get(self, request, *args, **kwargs):
        # Extract the 'ids' parameter from the query parameters
        ids = request.query_params.get('ids', '')

        # Split the 'ids' parameter by commas and convert to integers
        try:
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="TransferRequest",
            description="Invalid ID format in  request"
        )
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Query the Housekeeper objects with the given IDs
        housekeepers = TransferRequest.objects.filter(id__in=uuid_list)

        # Serialize the data
        serializer = TransferRequestSerializer(housekeepers, many=True)
        self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Retrieved",
            model_name="TransferRequest",
            description=f"Successfully retrieved {len(housekeepers)} TransferRequest for IDs: {ids}"
        )
        
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'ids',
                openapi.IN_QUERY,
                description="Comma-separated list of IDs",
                type=openapi.TYPE_STRING
            )
        ]
    )
    
    
    def delete(self, request, *args, **kwargs):
        # Extract the 'ids' parameter from the query parameters
        ids = request.query_params.get('ids', '')

        # Split the 'ids' parameter by commas and convert to integers
        try:
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
                user=request.user if request.user.is_authenticated else None,
                action_type="Error",
                model_name="TransferRequest",
                description="Invalid ID format in request"
            )
           
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the Housekeeper objects with the given IDs
        count, _ = TransferRequest.objects.filter(id__in=uuid_list).delete()
        
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Deleted",
        model_name="TransferRequest",
        description=f"Successfully deleted {count} TransferRequest for IDs: {ids}"
    )

        # Return the count of deleted objects
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
    
    
    
    
class TransferRequestListCreateView(ActionLoggingMixin,generics.ListCreateAPIView):
    queryset = TransferRequest.objects.all()
    serializer_class = TransferRequestSerializer
    permission_classes = [AllowAny] 
    
    def get(self, request, *args, **kwargs):
        # Log the action  
        user = request.user if request.user.is_authenticated else None
        self.log_action(
            user=user,
            action_type="Listed",
            model_name="TransferRequest"
        )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
    
        # Log the action
        user = request.user if request.user.is_authenticated else None
        self.log_action(
            user=user,
            action_type="Created",
            model_name="TransferRequest"
        )
        
        order_id = f"{serializer.instance.id}-{uuid.uuid4().hex[:8]}"
        serializer.instance.order_id = order_id
        serializer.instance.save()
        
        transfer_request_serializer = TransferRequestSerializer(serializer.instance)
    
    
        request_details = transfer_request_serializer.data.copy()  
        request_details['order_id'] = order_id 
    
        phone_number = serializer.validated_data.get('request_contact')
        test_mode = request.data.get('test_mode', False)
        success, message = send_message(phone_number, request_details, test_mode=test_mode)
    
        return Response({
        'message': message,
        'request_details': request_details  # Include all request details in the response
        }, status=status.HTTP_201_CREATED if success else status.HTTP_500_INTERNAL_SERVER_ERROR, headers=headers)
        
    #     test_mode = request.data.get('test_mode', False)
    #     # Retrieve request details
    #     request_details = {
    #         'housekeeper': serializer.validated_data.get('housekeeper'),
    #         'requester':serializer.validated_data.get('requester'),
    #         'requester_contact': serializer.validated_data.get('requester_contact'),
    #          'request_date': serializer.validated_data.get('request_date'),
    #         'status': serializer.validated_data.get('status'),
    #     }
        
    #     # Send notification to the requester with request details
    #     phone_number = serializer.validated_data.get('requester_contact')
    #     send_message(phone_number, request_details,test_mode=test_mode)
    #     print(send_message)
        
    #     success, message = send_message(phone_number, request_details, test_mode=test_mode)
    
    #     return Response({
    #     'message': message
    # }, status=status.HTTP_201_CREATED if success else status.HTTP_500_INTERNAL_SERVER_ERROR, headers=headers)

    

class TransferRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransferRequest.objects.all()
    serializer_class = TransferRequestSerializer
    permission_classes = [AllowAny] 
    

    
class TransferBatchStatusUpdateView(ActionLoggingMixin,APIView):
    serializer_class= UpdateHireRequest
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'ids',
                openapi.IN_QUERY,
                description="Comma-separated list of IDs",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="New status value",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    
    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        # Extract the 'ids' and 'status' parameters from the query parameters
        ids = request.query_params.get('ids', '')
        new_status_name = request.query_params.get('status', '')
        
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Patch Requested",
        model_name="TransferRequest",
        description=f"Patch request with IDs: {ids} and new status: {new_status_name}"
    )

        # Split the 'ids' parameter by commas and convert to integers
        try:
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
                user=request.user if request.user.is_authenticated else None,
                action_type="Error",
                model_name="TransferRequest",
                description="Invalid ID format in request"
            )
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        if not new_status_name:
            return Response({"error": "Status value is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Status object based on the provided status name
        try:
            new_status = Status.objects.get(Status=new_status_name)
        except Status.DoesNotExist:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="TransferRequest",
            description=f"Status '{new_status_name}' does not exist."
        )
            return Response({"error": f"Status '{new_status_name}' does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Query the Housekeeper objects with the given IDs
        Transfer = TransferRequest.objects.filter(id__in=uuid_list)

        if not Transfer.exists():
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="TransferRequest",
            description="No transfer Requests found for the provided IDs."
        )
            return Response({"error": "No Transfer Requests found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        # Update the status field for the queried Housekeeper objects
        Transfer.update(status=new_status)
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Updated",
        model_name="TransferRequest",
        description=f"Successfully updated status for IDs: {ids} to {new_status_name}"
    )
        
        for hire_request in Transfer:
            hire_request.status = new_status
            hire_request.save()  # Save to trigger the update

            if new_status.Status == "Approved":
                housekeeper = hire_request.housekeeper
                housekeeper.is_available = False
                housekeeper.save()
            else:
                housekeeper = hire_request.housekeeper
                housekeeper.is_available = True
                housekeeper.save()
            self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Updated",
        model_name="TransferRequest",
        description=f"Successfully updated status for IDs: {ids} to {new_status_name}"
    )
        
     
        return Response({"message": "Status updated successfully."}, status=status.HTTP_200_OK)
        
    
    
    
    

