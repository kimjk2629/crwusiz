#pragma once

#include <QLabel>
#include <QSlider>
#include <QWidget>

#include "selfdrive/ui/qt/widgets/cameraview.h"
#include "tools/replay/replay.h"

class Slider : public QSlider {
  Q_OBJECT

public:
  Slider(QWidget *parent);
  void mousePressEvent(QMouseEvent* e) override;
  void sliderChange(QAbstractSlider::SliderChange change) override;

signals:
  void setPosition(int value);

private:
   void paintEvent(QPaintEvent *ev) override;
   std::vector<std::tuple<int, int, TimelineType>> timeline;

  int slider_x = -1;
};

class VideoWidget : public QWidget {
  Q_OBJECT

public:
  VideoWidget(QWidget *parnet = nullptr);

protected:
  void rangeChanged(double min, double max);
  void updateState();
  void setPosition(int value);

  CameraViewWidget *cam_widget;
  QLabel *time_label, *total_time_label;
  Slider *slider;
};
