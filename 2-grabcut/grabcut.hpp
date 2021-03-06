#ifndef CV2_GRABCUT_HPP
#define CV2_GRABCUT_HPP

#include <opencv2/imgproc/imgproc.hpp>

namespace cv
{

/**
 * Constants for the connectivity of the graph used by
 * the GrabCut algorithm.
 */
enum
{
    GC_N4 = 4,
    GC_N8 = 8,
};

/**
 * Modified version of the GrabCut algorithm
 * 
 * @param tolerance     Take only this portion pixels in the rectangular for the
 *                      calculation of the foreground distribution that are most
 *                      unlikely in the background distribution.
 *                      
 * @param extended      Use an extended term for the pairwise / binary / smoothing
 *                      term
 * 
 * @param connectivity  Increases connectivity of the whole segmentation. If set
 *                      to infinity, the whole image will be one region.
 *
 * @param contrast      Boost segmentation in regions of high contrast
 * 
 * @param neighbors     Change the modeled connectivity of the graph used for the
 *                      min-cut calculation
 */
void extendedGrabCut(InputArray _img, InputOutputArray _mask, Rect rect,
                     InputOutputArray _bgdModel, InputOutputArray _fgdModel,
                     int iterCount, double tolerance = 1, bool extended = false,
                     double connectivity = 1, double contrast = 1,
                     int neighbors = GC_N8, int mode = GC_EVAL);

}


#endif // CV2_GRABCUT_HPP
