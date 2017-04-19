package controller

import (
	"time"

	"k8s.io/client-go/tools/cache"
	"k8s.io/client-go/util/flowcontrol"
	"k8s.io/client-go/util/workqueue"

	"github.com/openshift/origin/pkg/client"
	"github.com/openshift/origin/pkg/controller"
	"github.com/openshift/origin/pkg/controller/shared"
)

// NewImageStreamControllers creates an ImageStreamController and ScheduledImageStreamController.
func NewImageStreamControllers(
	isInformer shared.ImageStreamInformer,
	isNamespacer client.ImageStreamsNamespacer,
	checkInterval time.Duration,
	rateLimiter flowcontrol.RateLimiter,
	scheduleEnabled bool,
) (*ImageStreamController, *ScheduledImageStreamController) {

	// instantiate informer based image stream controller
	ctrl := newImageStreamController(isInformer, isNamespacer)

	// instantiate a scheduled importer using a number of buckets
	sched := newScheduledImageStreamController(isInformer, isNamespacer, rateLimiter, checkInterval, scheduleEnabled)

	// setup notifier on the main controller so that it informs the scheduled
	// controller when streams are being imported
	ctrl.notifier = sched

	return ctrl, sched
}

func newImageStreamController(isInformer shared.ImageStreamInformer, isNamespacer client.ImageStreamsNamespacer) *ImageStreamController {
	ctrl := &ImageStreamController{
		queue: workqueue.NewRateLimitingQueue(workqueue.DefaultControllerRateLimiter()),

		isNamespacer: isNamespacer,
		lister:       temporaryLister{isInformer.Lister()},
		listerSynced: isInformer.Informer().HasSynced,
	}

	isInformer.Informer().AddEventHandler(cache.ResourceEventHandlerFuncs{
		AddFunc:    ctrl.addImageStream,
		UpdateFunc: ctrl.updateImageStream,
	})

	return ctrl
}

func newScheduledImageStreamController(
	isInformer shared.ImageStreamInformer,
	isNamespacer client.ImageStreamsNamespacer,
	rateLimiter flowcontrol.RateLimiter,
	checkInterval time.Duration,
	scheduleEnabled bool,
) *ScheduledImageStreamController {
	buckets := 4
	switch {
	case checkInterval > time.Hour:
		buckets = 8
	case checkInterval < 10*time.Minute:
		buckets = 2
	}
	seconds := checkInterval / time.Second
	bucketQPS := 1.0 / float32(seconds) * float32(buckets)
	bucketLimiter := flowcontrol.NewTokenBucketRateLimiter(bucketQPS, 1)

	sched := &ScheduledImageStreamController{
		enabled:     scheduleEnabled,
		rateLimiter: rateLimiter,

		isNamespacer: isNamespacer,
		lister:       temporaryLister{isInformer.Lister()},
		listerSynced: isInformer.Informer().HasSynced,
	}
	sched.scheduler = controller.NewScheduler(buckets, bucketLimiter, sched.syncTimed)

	isInformer.Informer().AddEventHandler(cache.ResourceEventHandlerFuncs{
		AddFunc:    sched.addImageStream,
		UpdateFunc: sched.updateImageStream,
		DeleteFunc: sched.deleteImageStream,
	})

	return sched
}
