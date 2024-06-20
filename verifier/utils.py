from .models import CustomUser, VerificationTaskResult, TaskObject
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



def assign_task_to_verifier():
    tasks = TaskObject.objects.filter(state=TaskObject.PENDING)
    available_verifiers = CustomUser.objects.filter(is_available=True, is_annotator=True)

    if tasks and available_verifiers:
        for task in tasks:
            for verifier in available_verifiers:
                result_task, created = VerificationTaskResult.objects.get_or_create(task=task, tagged_by=verifier, completed=False)

                print("hereee", created)

                if created:
                    # Notify verifier via WebSocket
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        f"user_{verifier.id}",
                        {
                            "type": "task_assign",
                            "task_id": task.id,
                            "image_url": task.image.url if task.image else None,
                            "details": task.details,
                            "options": task.options
                        }
                    )
                    print("Task assigned to verifier", f"user_{verifier.id}")
                    break  # Assign to only one verifier for now
