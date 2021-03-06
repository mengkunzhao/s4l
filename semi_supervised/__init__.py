# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generates training data with self supervision.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

from semi_supervised import exemplar
# xcxc from semi_supervised import exemplar_ablation
from semi_supervised import rotation
# xcxc from semi_supervised import rotation_ablation
from semi_supervised import rotation_vat
from semi_supervised import supervised
from semi_supervised import vat


def get_model(self_supervision):
  """Gets self supervised training data and labels."""

  mapping = {
      "exemplar": exemplar.model_fn,
      # "exemplar_ablation": exemplar_ablation.model_fn,
      "rotation": rotation.model_fn,
      # "rotation_ablation": rotation_ablation.model_fn,
      "rotation_vat": rotation_vat.model_fn,
      "supervised": supervised.model_fn,
      "vat": vat.model_fn,
  }

  model_fn = mapping.get(self_supervision)
  if model_fn is None:
    raise ValueError("Unknown self-supervision: %s" % self_supervision)

  def _model_fn(features, labels, mode, params):
    """Returns the EstimatorSpec to run the model.

    Args:
      features: Dict of inputs ("image" being the image).
      labels: unused but required by Estimator API.
      mode: model's mode: training, eval or prediction
      params: required by Estimator API, contains TPU local `batch_size`.

    Returns:
      EstimatorSpec

    Raises:
      ValueError when the self_supervision is unknown.
    """
    del labels, params  # unused
    tf.logging.info("Calling model_fn in mode %s with data:", mode)
    tf.logging.info(features)
    return model_fn(features, mode)

  return _model_fn
