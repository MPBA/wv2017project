class Generator(object):
    def __init__(self, gt, bbox_util,
                 batch_size, path_prefix,
                 train_keys, val_keys, image_size,
                 saturation_var=0.5,
                 brightness_var=0.5,
                 contrast_var=0.5,
                 lighting_std=0.5,
                 saturation_prob=0.5,
                 brightness_prob=0.5,
                 contrast_prob=0.5,
                 lighting_prob=0.5,
                 hflip_prob=0.5,
                 vflip_prob=0.5):
        self.gt = gt
        self.bbox_util = bbox_util
        self.batch_size = batch_size
        self.path_prefix = path_prefix
        self.train_keys = train_keys
        self.val_keys = val_keys
        self.train_batches = len(train_keys)
        self.val_batches = len(val_keys)
        self.image_size = image_size
        self.color_jitter = []
        if saturation_var:
            self.saturation_var = saturation_var
            self.color_jitter.append(self.saturation)
        if brightness_var:
            self.brightness_var = brightness_var
            self.color_jitter.append(self.brightness)
        if contrast_var:
            self.contrast_var = contrast_var
            self.color_jitter.append(self.contrast)
        self.lighting_std = lighting_std
        self.hflip_prob = hflip_prob
        self.vflip_prob = vflip_prob

    def grayscale(self, rgb):
        rgb.dot([0.299, 0.587, 0.114])
        return rgb

    def saturation(self, rgb):
        if np.random.random() < self.hflip_prob:
            gs = self.grayscale(rgb)
            alpha = 2 * np.random.random() * self.saturation_var
            alpha += 1 - self.saturation_var
            rgb = rgb * alpha + (1 - alpha) * gs[:, :, None]
            rgb =  np.clip(rgb, 0, 255)
        return rgb

    def brightness(self, rgb):
        if np.random.random() < self.hflip_prob:
            alpha = 2 * np.random.random() * self.brightness_var
            alpha += 1 - self.saturation_var
            rgb = rgb * alpha
            rgb = np.clip(rgb, 0, 255)
        return rgb

    def contrast(self, rgb):
        if np.random.random() < self.hflip_prob:
            gs = self.grayscale(rgb).mean() * np.ones_like(rgb)
            alpha = 2 * np.random.random() * self.contrast_var
            alpha += 1 - self.contrast_var
            rgb = rgb * alpha + (1 - alpha) * gs
            rgb = np.clip(rgb, 0, 255)
        return rgb

    def lighting(self, img):
        if np.random.random() < self.lighting_prob:
            cov = np.cov(img.reshape(-1, 3) / 255.0, rowvar=False)
            eigval, eigvec = np.linalg.eigh(cov)
            noise = np.random.randn(3) * self.lighting_std
            noise = eigvec.dot(eigval * noise) * 255
            img += noise
            img = np.clip(img, 0, 255)
        return img

    def flipH(self, X, y):
        if np.random.random() < self.vflip_prob:
            for idx in range(len(X)):
                X[idx] = np.fliplr(X[idx])

            for idx, image in enumerate(y):
                _,imWidth,_=X[idx].shape
                for ann in image:
                    ann['x']=imWidth-ann['x']-ann['width']
        return X, y


    def flipV(self, X, y):
        if np.random.random() < self.vflip_prob:
            for idx in range(len()):
                [idx] = np.flipud([idx])

            for idx, image in enumerate(y):
                imHeight,_,_=[idx].shape
                for ann in image:
                    ann['y']=imHeight-ann['y']-ann['height']
        return X, y

    def generate(self, train=True):
        while True:
            if train:
                shuffle(self.train_keys)
                keys = self.train_keys
            else:
                shuffle(self.val_keys)
                keys = self.val_keys
            inputs = []
            targets = []
            for key in keys:
                img_path = self.path_prefix + key
                img = imread(img_path).astype('float32')
                y = self.gt[key].copy()
                if train and self.do_crop:
                    img, y = self.random_sized_crop(img, y)
                img = imresize(img, self.image_size).astype('float32')
                if train:
                    shuffle(self.color_jitter)
                    for jitter in self.color_jitter:
                        img = jitter(img)
                    if self.lighting_std:
                        img = self.lighting(img)
                    if self.hflip_prob > 0:
                        img, y = self.horizontal_flip(img, y)
                    if self.vflip_prob > 0:
                        img, y = self.vertical_flip(img, y)
                y = self.bbox_util.assign_boxes(y)
                inputs.append(img)
                targets.append(y)
                if len(targets) == self.batch_size:
                    tmp_inp = np.array(inputs)
                    tmp_targets = np.array(targets)
                    inputs = []
                    targets = []
                    yield preprocess_input(tmp_inp), tmp_targets
