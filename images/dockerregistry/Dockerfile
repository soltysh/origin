#
# This is the integrated OpenShift Docker registry. It is configured to
# publish metadata to OpenShift to provide automatic management of images on push.
#
# The standard name for this image is openshift3/ose-dockerregistry
#
FROM openshift3/origin-base

RUN INSTALL_PKGS="origin-dockerregistry" && \
    yum install -y $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    yum clean all

COPY config.yml $REGISTRY_CONFIGURATION_PATH

LABEL io.k8s.display-name="OpenShift Image Registry" \
      io.k8s.description="This is a component of OpenShift and exposes a Docker registry that is integrated with the cluster for authentication and management." \
      io.openshift.tags="openshift,docker,registry"

# The registry doesn't require a root user.
USER 1001
EXPOSE 5000
VOLUME /registry
ENV REGISTRY_CONFIGURATION_PATH=/config.yml

CMD DOCKER_REGISTRY_URL=${DOCKER_REGISTRY_SERVICE_HOST}:${DOCKER_REGISTRY_SERVICE_PORT} /usr/bin/dockerregistry ${REGISTRY_CONFIGURATION_PATH}
